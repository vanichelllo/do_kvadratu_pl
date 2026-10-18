import uuid
import datetime
from django.contrib import admin
from django.contrib import messages
from django.db.models import BooleanField, Case, Count, Q, Value, When
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html

# Імпорти для вивантаження бази в Excel
from import_export import resources
from import_export.admin import ExportActionMixin
from django import forms
from django.contrib.auth import get_user_model

from users.models import PurchaseHistory
from .bank_import import (MAX_FILE_BYTES, SPEC_KEYS, BankFormatError, build_report, import_tasks, parse_bank_source,
                          validate_school_spec)
from .practice import describe_correct
from .models import (
    StudyMaterial, Tag, Cart, CartItem, DiagnosticOffer, Order, OrderItem,
    Question, AnswerOption, MatchItem, TutorStudentRequest,
    Review, StudentPresentation, QuestionError, StudentReport,
    CurriculumSubject, CurriculumGrade, CurriculumChapter, CurriculumTopic
)

User = get_user_model()

@admin.register(CurriculumSubject)
class CurriculumSubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order',)

@admin.register(CurriculumGrade)
class CurriculumGradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'order')
    list_filter = ('subject',)
    ordering = ('subject__order', 'order')

@admin.register(CurriculumChapter)
class CurriculumChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'order')
    list_select_related = ('grade__subject',)
    list_filter = ('grade__subject', 'grade')
    search_fields = ('name',)

@admin.register(CurriculumTopic)
class CurriculumTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter', 'order')
    list_select_related = ('chapter__grade__subject',)
    list_filter = ('chapter__grade__subject', 'chapter__grade')
    # Пошук і за курсом/класом: «11 клас логарифм» знаходить тему лише з потрібного класу
    search_fields = ('name', 'chapter__name', 'chapter__grade__name', 'chapter__grade__subject__name')

    def get_queryset(self, request):
        # Назва теми містить курс і клас — підтягуємо їх одним запитом (і для пошуку в автодоповненні)
        return super().get_queryset(request).select_related('chapter__grade__subject')

@admin.action(description="✅ Підтвердити статус (та видати курс для НМТ)")
def approve_student_requests(modeladmin, request, queryset):
    # ОНОВЛЕНО: Шукаємо всі матеріали НМТ за новим класифікатором
    nmt_materials = StudyMaterial.objects.filter(
        curriculum_topic__chapter__grade__subject__name="Підготовка до НМТ / ЗНО",
        is_published=True
    )

    count = 0
    for student_request in queryset.filter(status='pending'):
        student_request.status = 'approved'
        student_request.save()

        if student_request.course == 'nmt':
            for material in nmt_materials:
                student_request.user.purchased_materials.add(material)

        count += 1

    messages.success(request, f"Успішно підтверджено заявок: {count}.")


@admin.action(description="❌ Відхилити заявки")
def reject_student_requests(modeladmin, request, queryset):
    queryset.update(status='rejected')


def materials_paid_by(user):
    paid_ids = set(OrderItem.objects.filter(order__user=user, order__status='paid', material__isnull=False)
                   .values_list('material_id', flat=True))
    paid_ids |= set(PurchaseHistory.objects.filter(student=user, material__isnull=False)
                    .values_list('material_id', flat=True))
    paid_ids |= set(StudyMaterial.included_materials.through.objects.filter(from_studymaterial_id__in=paid_ids)
                    .values_list('to_studymaterial_id', flat=True))
    return paid_ids


@admin.action(description="🗑 Забрати доступ (Видалити з учнів)")
def revoke_student_access(modeladmin, request, queryset):
    # ОНОВЛЕНО: Знаходимо всі НМТ-матеріали за новим класифікатором
    nmt_materials = StudyMaterial.objects.filter(
        curriculum_topic__chapter__grade__subject__name="Підготовка до НМТ / ЗНО"
    )

    count = 0
    kept_all = []
    for student_request in queryset:
        user = student_request.user
        if (OrderItem.objects.filter(order__user=user, order__status='paid', material__isnull=True).exists()
                or PurchaseHistory.objects.filter(student=user, material__isnull=True).exists()):
            kept_all.append(student_request.real_name)
        else:
            keep_ids = materials_paid_by(user)
            to_remove = nmt_materials.exclude(id__in=keep_ids).exclude(is_free=True).exclude(price=0)
            user.purchased_materials.remove(*to_remove)

        student_request.delete()
        count += 1

    messages.success(request, f"Успішно видалено {count} учнів. Видані на час навчання матеріали НМТ забрано, "
                              f"куплені учнем самостійно — залишились.")
    if kept_all:
        messages.warning(request, "Матеріали не забирали (серед їхніх оплат є видалений матеріал чи пакет, "
                                  "тож не видно, що саме оплачено): " + ", ".join(kept_all)
                         + ". Перевірте доступ цих учнів вручну.")


@admin.action(description="🔑 Створити нове посилання для батьків (старе перестане працювати)")
def regenerate_parent_links(modeladmin, request, queryset):
    count = 0
    for student_request in queryset:
        student_request.parent_token = uuid.uuid4()
        student_request.save(update_fields=['parent_token'])
        count += 1
    messages.success(request, f"Нові посилання створено: {count}. Старі більше не відкриваються — "
                              f"скопіюйте нові в кабінеті й надішліть батькам.")


@admin.register(TutorStudentRequest)
class TutorStudentRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'real_name', 'course', 'status', 'created_at', 'parent_token')
    list_select_related = ('user',)
    list_filter = ('course', 'status', 'created_at')
    search_fields = ('user__email', 'real_name')
    readonly_fields = ('parent_token',)
    actions = [approve_student_requests, reject_student_requests, revoke_student_access, regenerate_parent_links]


# ==========================================
# НУШ ЗВІТИ ДЛЯ БАТЬКІВ
# ==========================================
@admin.register(StudentReport)
class StudentReportAdmin(admin.ModelAdmin):
    # ОНОВЛЕНО: curriculum_topic замість topic
    list_display = ('student', 'date', 'curriculum_topic', 'homework_status')
    list_select_related = ('student', 'curriculum_topic__chapter__grade__subject')
    autocomplete_fields = ['curriculum_topic']
    list_filter = ('date', 'homework_status', 'student__course')
    search_fields = ('student__real_name', 'curriculum_topic__name', 'teacher_comment')


admin.site.register(Tag)

# ==========================================
# ДІАГНОСТИЧНИЙ ТЕСТ: ПИТАННЯ ТА ВІДПОВІДІ
# ==========================================
class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 5


class MatchItemInline(admin.TabularInline):
    model = MatchItem
    extra = 3

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'correct_option':
            question_id = getattr(request, '_admin_question_id', None)
            kwargs['queryset'] = (AnswerOption.objects.filter(question_id=question_id) if question_id
                                  else AnswerOption.objects.none())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


GRADE_FILTER_PARAM = 'curriculum_topic__chapter__grade__id__exact'


class TopicOfGradeFilter(admin.SimpleListFilter):
    """Теми з'являються після вибору класу — лише теми цього класу, а не всі сотні."""
    title = 'тема (спершу оберіть клас)'
    parameter_name = 'topic'

    def lookups(self, request, model_admin):
        grade_id = request.GET.get(GRADE_FILTER_PARAM)
        if not grade_id or not grade_id.isdigit():
            return []
        return [(topic.id, topic.name) for topic in CurriculumTopic.objects.filter(chapter__grade_id=grade_id)]

    def queryset(self, request, queryset):
        if self.value() and self.value().isdigit():
            return queryset.filter(curriculum_topic_id=self.value())
        return queryset


class DuplicateTextFilter(admin.SimpleListFilter):
    """Завдання з однаковим текстом (без урахування пробілів) — поруч, щоб прибрати зайву копію.
    Менший ID — старіша копія. Загальні умови на кшталт «Узгодьте вираз (1–3) …» теж потраплять сюди,
    тож перед видаленням порівняйте варіанти."""
    title = 'повтор тексту'
    parameter_name = 'dup'

    def lookups(self, request, model_admin):
        return [('yes', 'Є завдання з таким самим текстом')]

    def queryset(self, request, queryset):
        if self.value() != 'yes':
            return queryset
        groups = {}
        for pk, text in Question.objects.values_list('id', 'text'):
            groups.setdefault(' '.join(text.split()), []).append(pk)
        ids = [pk for pks in groups.values() if len(pks) > 1 for pk in pks]
        return queryset.filter(id__in=ids).order_by('text', 'id')


class HasPictureFilter(admin.SimpleListFilter):
    title = 'малюнок'
    parameter_name = 'picture'

    def lookups(self, request, model_admin):
        return [('yes', 'З малюнком'), ('no', 'Без малюнка')]

    def queryset(self, request, queryset):
        has_picture = (Q(svg_code__isnull=False) & ~Q(svg_code__regex=r'^\s*$')) | (Q(image__isnull=False) & ~Q(image=''))
        if self.value() == 'yes':
            return queryset.filter(has_picture)
        if self.value() == 'no':
            return queryset.exclude(has_picture)
        return queryset


class HasTopicFilter(admin.EmptyFieldListFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'наявність теми'


class QuestionBulkEditForm(forms.Form):
    curriculum_topic = forms.ModelChoiceField(
        CurriculumTopic.objects.select_related('chapter__grade__subject'), required=False, label='Нова тема')
    difficulty = forms.TypedChoiceField(choices=[('', '— не змінювати —')] + list(Question.DIFFICULTY_CHOICES),
                                        coerce=int, empty_value=None, required=False, label='Нова складність')
    add_material = forms.ModelChoiceField(StudyMaterial.objects.filter(is_bundle=False), required=False,
                                          label='Додати до уроку')
    remove_material = forms.ModelChoiceField(StudyMaterial.objects.filter(is_bundle=False), required=False,
                                             label='Прибрати з уроку')


@admin.action(description='✏️ Змінити позначені завдання (тема, складність, урок)…')
def bulk_edit_questions(modeladmin, request, queryset):
    if request.POST.get('apply'):
        form = QuestionBulkEditForm(request.POST)
        if form.is_valid():
            data, changes = form.cleaned_data, []
            if data['curriculum_topic']:
                queryset.update(curriculum_topic=data['curriculum_topic'])
                changes.append(f"тема → {data['curriculum_topic'].name}")
            if data['difficulty']:
                queryset.update(difficulty=data['difficulty'])
                changes.append(f"складність → {dict(Question.DIFFICULTY_CHOICES)[data['difficulty']]}")
            if data['add_material']:
                data['add_material'].practice_questions.add(*queryset)
                changes.append(f"додано до «{data['add_material'].title}»")
            if data['remove_material']:
                data['remove_material'].practice_questions.remove(*queryset)
                changes.append(f"прибрано з «{data['remove_material'].title}»")
            if changes:
                messages.success(request, f"Змінено завдань: {queryset.count()} ({'; '.join(changes)}).")
            else:
                messages.warning(request, 'Нічого не обрано для зміни — завдання не змінено.')
            return None
    else:
        form = QuestionBulkEditForm()
    return render(request, 'admin/materials/question/bulk_edit.html', {
        **modeladmin.admin_site.each_context(request), 'opts': modeladmin.model._meta,
        'title': 'Змінити позначені завдання', 'form': form, 'questions': queryset,
        'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
    })


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'id', 'topic_name', 'question_type', 'difficulty', 'health')
    list_select_related = ('curriculum_topic',)
    list_filter = ('curriculum_topic__chapter__grade', TopicOfGradeFilter,
                   ('curriculum_topic', HasTopicFilter), 'question_type', 'difficulty', 'nush_skill', HasPictureFilter, DuplicateTextFilter)
    # Пошук і за назвою теми: «21» або «логарифм»
    search_fields = ('text', 'curriculum_topic__name')
    autocomplete_fields = ['curriculum_topic']
    actions = [bulk_edit_questions]
    readonly_fields = ('preview',)
    fieldsets = (
        (None, {'fields': ('text', 'question_type', 'difficulty', 'curriculum_topic', 'materials', 'image',
                           'svg_code', 'correct_short_answer')}),
        ('Шкільна практика (5–11 класи)', {'fields': ('nush_skill', 'hint', 'solution', 'spec')}),
        ('Попередній перегляд (збережена версія)', {'fields': ('preview',)}),
    )
    filter_horizontal = ('materials',)
    inlines = [MatchItemInline, AnswerOptionInline]
    change_list_template = 'admin/materials/question/change_list.html'

    def get_urls(self):
        custom = [path('import-bank/', self.admin_site.admin_view(self.import_bank_view),
                       name='materials_question_import_bank')]
        return custom + super().get_urls()

    def import_bank_view(self, request):
        if not self.has_add_permission(request):
            raise PermissionDenied

        session_key = 'bank_import_pending'
        context = {**self.admin_site.each_context(request), 'opts': self.model._meta,
                   'title': 'Завантажити завдання', 'max_mb': MAX_FILE_BYTES // (1024 * 1024)}

        if request.method == 'POST' and request.POST.get('action') == 'import':
            pending = request.session.get(session_key)
            if not pending:
                messages.error(request, 'Пробний звіт застарів — завантажте файл ще раз.')
                return redirect('admin:materials_question_import_bank')
            try:
                topic_name, tasks = parse_bank_source(pending['source'])
            except BankFormatError as exc:
                messages.error(request, str(exc))
                return redirect('admin:materials_question_import_bank')
            report, added = import_tasks(topic_name, tasks)
            request.session.pop(session_key, None)
            messages.success(request, f'Імпортовано завдань: {added}. Дублікатів пропущено: '
                                      f'{len(report.duplicates)}, з помилками пропущено: {len(report.errors)}.')
            return redirect('admin:materials_question_changelist')

        if request.method == 'POST':
            upload = request.FILES.get('bank_file')
            error = None
            if not upload:
                error = 'Оберіть файл.'
            elif upload.size > MAX_FILE_BYTES:
                error = f'Файл завеликий (максимум {MAX_FILE_BYTES // (1024 * 1024)} МБ).'
            else:
                try:
                    source = upload.read().decode('utf-8-sig')
                    topic_name, tasks = parse_bank_source(source)
                except UnicodeDecodeError:
                    error = 'Файл має бути у кодуванні UTF-8.'
                except BankFormatError as exc:
                    error = str(exc)
            if error:
                request.session.pop(session_key, None)
                context['error'] = error
            else:
                request.session[session_key] = {'name': upload.name, 'source': source}
                context.update(report=build_report(topic_name, tasks), file_name=upload.name)
        return render(request, 'admin/materials/question/import_bank.html', context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        request._admin_question_id = object_id
        return super().change_view(request, object_id, form_url, extra_context)

    class Media:
        # Формули $…$ у списку, попередньому перегляді й масовому редагуванні відмальовуються MathJax
        js = ('materials/admin_mathjax.js',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            n_options=Count('options', distinct=True),
            n_correct=Count('options', filter=Q(options__is_correct=True), distinct=True),
            n_pairs=Count('match_items', distinct=True))

    @admin.display(description='Текст', ordering='text')
    def short_text(self, obj):
        return obj.text if len(obj.text) <= 120 else obj.text[:117] + '…'

    @admin.display(description='Тема', ordering='curriculum_topic__name')
    def topic_name(self, obj):
        return obj.curriculum_topic.name if obj.curriculum_topic else '—'

    @admin.display(description='Перевірка')
    def health(self, obj):
        problem = question_problem(obj, obj.n_options, obj.n_correct, obj.n_pairs)
        return f'⚠ {problem}' if problem else '✓'

    @admin.display(description='Як бачить учень')
    def preview(self, obj):
        if not obj.pk:
            return 'Попередній перегляд з\'явиться після збереження.'
        return render_to_string('admin/materials/question/preview.html', {
            'question': obj, 'options': obj.options.all(),
            'pairs': obj.match_items.select_related('correct_option'),
            'problem': question_problem(obj, obj.options.count(), obj.options.filter(is_correct=True).count(),
                                        obj.match_items.count()),
            'school_answer': describe_correct(obj) if obj.question_type in SPEC_KEYS else '',
        })


def question_problem(question, n_options, n_correct, n_pairs):
    """Чому завдання не можна нормально розв'язати, або None."""
    if question.question_type == 'CHOICE':
        if n_options < 2:
            return 'менше двох варіантів'
        if n_correct != 1:
            return 'має бути рівно одна правильна відповідь'
    elif question.question_type == 'MATCH':
        if not n_pairs:
            return 'немає пар відповідності'
        if n_options < n_pairs:
            return 'варіантів менше, ніж пар'
    elif question.question_type == 'SHORT' and not (question.correct_short_answer or '').strip():
        return 'немає правильної відповіді'
    elif question.question_type in SPEC_KEYS:
        spec = question.spec if isinstance(question.spec, dict) else {}
        problems = validate_school_spec(question.question_type, spec)
        return problems[0] if problems else None
    return None


# ==========================================
# ВІТРИНА: МАТЕРІАЛИ ТА ІМПОРТ
# ==========================================
class HasPresentationFilter(admin.SimpleListFilter):
    title = 'HTML-презентація'
    parameter_name = 'has_html'

    def lookups(self, request, model_admin):
        return (('yes', 'Є'), ('no', 'Немає'))

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(has_html=True)
        if self.value() == 'no':
            return queryset.filter(has_html=False)
        return queryset


class HasPdfFilter(admin.SimpleListFilter):
    title = 'PDF-файл'
    parameter_name = 'has_pdf'

    def lookups(self, request, model_admin):
        return (('yes', 'Є'), ('no', 'Немає'))

    def queryset(self, request, queryset):
        no_file = Q(file__isnull=True) | Q(file='')
        if self.value() == 'yes':
            return queryset.exclude(no_file)
        if self.value() == 'no':
            return queryset.filter(no_file)
        return queryset


MAX_HTML_UPLOAD_BYTES = 5 * 1024 * 1024


class StudyMaterialAdminForm(forms.ModelForm):
    html_file = forms.FileField(
        required=False, label='Завантажити .html',
        help_text='Вміст файлу замінить HTML-презентацію. Без файлу презентація не змінюється.')

    class Meta:
        model = StudyMaterial
        fields = '__all__'

    def clean_html_file(self):
        upload = self.cleaned_data.get('html_file')
        if not upload:
            return None
        if not upload.name.lower().endswith(('.html', '.htm')):
            raise forms.ValidationError('Потрібен файл .html')
        if upload.size > MAX_HTML_UPLOAD_BYTES:
            raise forms.ValidationError(f'Файл завеликий (максимум {MAX_HTML_UPLOAD_BYTES // (1024 * 1024)} МБ).')
        try:
            return upload.read().decode('utf-8-sig')
        except UnicodeDecodeError:
            raise forms.ValidationError('Файл має бути у кодуванні UTF-8.')

    def save(self, commit=True):
        html = self.cleaned_data.get('html_file')
        if html:
            self.instance.html_content = html
        return super().save(commit)


class StudyMaterialAdmin(admin.ModelAdmin):
    form = StudyMaterialAdminForm
    list_display = ('title', 'grade_label', 'price', 'is_published', 'is_free', 'is_bundle', 'has_html', 'has_pdf')
    list_display_links = ('title',)
    # Ціну й публікацію можна змінити прямо в списку і зберегти кнопкою внизу
    list_editable = ('price', 'is_published')
    list_select_related = ('curriculum_topic__chapter__grade__subject',)
    list_filter = ('is_published', 'is_free', 'is_bundle', HasPresentationFilter, HasPdfFilter,
                   'curriculum_topic__chapter__grade')
    search_fields = ('title',)
    autocomplete_fields = ['curriculum_topic']
    # Два списки з пошуком замість множинного вибору з Ctrl
    filter_horizontal = ('included_materials', 'tags')
    readonly_fields = ('reader_link',)
    fieldsets = (
        ('Основне', {'fields': ('title', 'curriculum_topic', 'tags', 'description')}),
        ('Вітрина', {'fields': ('price', 'is_free', 'is_published', 'image')}),
        ('Контент', {'fields': ('file', 'html_file', 'reader_link')}),
        ('HTML-код вручну', {'classes': ('collapse',), 'fields': ('html_content',),
                             'description': 'Зручніше завантажити файл у блоці «Контент» вище.'}),
        ('Пакет', {'classes': ('collapse',), 'fields': ('is_bundle', 'included_materials')}),
    )

    def get_fieldsets(self, request, obj=None):
        # Склад пакета згорнутий для звичайних матеріалів, але одразу видно, коли редагуємо пакет
        if obj is not None and obj.is_bundle:
            return [(name, {**options, 'classes': ()}) if name == 'Пакет' else (name, options)
                    for name, options in self.fieldsets]
        return self.fieldsets

    @admin.display(description='Перевірити')
    def reader_link(self, obj):
        if not obj.pk:
            return 'Посилання з\'явиться після збереження.'
        return format_html('<a href="{}" target="_blank">📖 Відкрити в читалці</a> (так, як бачить учень)',
                           reverse('download_material', args=[obj.pk]))

    def get_queryset(self, request):
        # Презентація (до кількох МБ) у списку не завантажується — лише позначка, чи вона є
        filled = Q(html_content__isnull=False) & ~Q(html_content='')
        return super().get_queryset(request).annotate(
            has_html=Case(When(filled, then=Value(True)), default=Value(False), output_field=BooleanField()))

    @admin.display(description='Курс / клас', ordering='curriculum_topic__chapter__grade__order')
    def grade_label(self, obj):
        grade = obj.curriculum_grade
        return grade.short_label if grade else '—'

    @admin.display(description='HTML', boolean=True, ordering='has_html')
    def has_html(self, obj):
        return obj.has_html

    @admin.display(description='PDF', boolean=True)
    def has_pdf(self, obj):
        return bool(obj.file)

admin.site.register(StudyMaterial, StudyMaterialAdmin)


# ==========================================
# КОМЕРЦІЯ: КОШИК ТА ЗАМОВЛЕННЯ
# ==========================================
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    inlines = [CartItemInline]


@admin.register(DiagnosticOffer)
class DiagnosticOfferAdmin(admin.ModelAdmin):
    """Хто отримав знижку на пакет слабких тем після діагностики і до коли вона діє."""
    list_display = ['user', 'discount_percent', 'created_at', 'expires_at']
    list_select_related = ['user']
    search_fields = ['user__email']
    autocomplete_fields = ['user']
    filter_horizontal = ['materials']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id', 'created_at', 'customer_email', 'source', 'status', 'total_amount')
        export_order = ('id', 'created_at', 'customer_email', 'source', 'status', 'total_amount')

@admin.register(Order)
class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = OrderResource

    list_display = ['id', 'user', 'customer_email', 'total_amount', 'status', 'source', 'created_at', 'paid_at']
    list_filter = ['status', 'source', 'created_at']
    search_fields = ['user__email', 'customer_email', 'mono_invoice_id']
    inlines = [OrderItemInline]
    actions = ['check_monobank_status']
    readonly_fields = ['instant_access_agreed_at']

    @admin.action(description="🔄 Перевірити статус у Monobank (для «Очікує оплати» і «Скасовано»)")
    def check_monobank_status(self, request, queryset):
        from .views import check_mono_invoice
        checked = 0
        for order in (queryset.filter(status__in=['pending', 'cancelled'])
                      .exclude(mono_invoice_id__isnull=True).exclude(mono_invoice_id='')):
            check_mono_invoice(order)
            checked += 1
        self.message_user(request, f"Перевірено замовлень: {checked}. Статуси оновлено відповідно до Monobank.")


# ==========================================
# ВІДГУКИ
# ==========================================
@admin.action(description="✅ Схвалити вибрані відгуки (показувати на сайті)")
def approve_reviews(modeladmin, request, queryset):
    queryset.update(is_approved=True)
    messages.success(request, "Вибрані відгуки успішно схвалено та опубліковано!")

@admin.action(description="❌ Приховати вибрані відгуки")
def hide_reviews(modeladmin, request, queryset):
    queryset.update(is_approved=False)
    messages.warning(request, "Вибрані відгуки приховано із сайту.")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'material', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('user__email', 'text')
    actions = [approve_reviews, hide_reviews]


class ApprovedStudentChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if hasattr(obj, 'tutor_request') and obj.tutor_request:
            return f"{obj.tutor_request.real_name} ({obj.email})"
        return obj.email

@admin.register(StudentPresentation)
class StudentPresentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'created_at')
    search_fields = ('title', 'student__email', 'student__tutor_request__real_name')
    list_filter = ('created_at',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = User.objects.filter(tutor_request__status='approved')
            kwargs["form_class"] = ApprovedStudentChoiceField
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(QuestionError)
class QuestionErrorAdmin(admin.ModelAdmin):
    list_display = ('question', 'question_link', 'user', 'status', 'created_at')
    list_select_related = ('question', 'user')
    readonly_fields = ('question_link',)

    @admin.display(description='Завдання в адмінці')
    def question_link(self, obj):
        return format_html('<a href="{}">✏️ Відкрити завдання</a>',
                           reverse('admin:materials_question_change', args=[obj.question_id]))
    list_filter = ('status', 'created_at')
    search_fields = ('message', 'question__text')

# ==========================================
# ЗАГОЛОВОК І ПОРЯДОК РОЗДІЛІВ АДМІНКИ
# ==========================================
admin.site.site_header = 'ДО КВАДРАТУ — адмінка'
admin.site.site_title = 'ДО КВАДРАТУ'
admin.site.index_title = 'Керування платформою'

# Спершу щоденна робота, далі класифікатор, службове — в кінці. Не вказані тут моделі й застосунки йдуть після
APP_ORDER = ['materials', 'users', 'telegram_bot', 'account', 'socialaccount', 'auth', 'sites']
MODEL_ORDER = [
    'StudyMaterial', 'Question', 'TutorStudentRequest', 'StudentReport', 'StudentPresentation', 'Order', 'Review',
    'QuestionError', 'Tag', 'CurriculumSubject', 'CurriculumGrade', 'CurriculumChapter', 'CurriculumTopic', 'Cart',
    'CustomUser', 'PurchaseHistory',
]
_default_get_app_list = admin.site.get_app_list


def ordered_app_list(request, app_label=None):
    def position(order, key):
        return order.index(key) if key in order else len(order)

    app_list = _default_get_app_list(request, app_label)
    for app in app_list:
        app['models'].sort(key=lambda model: position(MODEL_ORDER, model['object_name']))
    app_list.sort(key=lambda app: position(APP_ORDER, app['app_label']))
    return app_list


admin.site.get_app_list = ordered_app_list


# ==========================================
# ГОЛОВНА АДМІНКИ: «ПОТРЕБУЄ УВАГИ»
# ==========================================
def attention_items(request):
    """Що варто переглянути: кількість і посилання на вже відфільтрований список."""
    from telegram_bot.models import BotLead

    no_html = Q(html_content__isnull=True) | Q(html_content='')
    checks = [
        ('Нові заявки на статус учня', TutorStudentRequest.objects.filter(status='pending'),
         'materials.tutorstudentrequest', 'status__exact=pending'),
        ('Нові заявки з бота', BotLead.objects.filter(processed=False),
         'telegram_bot.botlead', 'processed__exact=0'),
        ('Нові скарги на завдання', QuestionError.objects.filter(status='new'),
         'materials.questionerror', 'status__exact=new'),
        ('Відгуки чекають модерації', Review.objects.filter(is_approved=False),
         'materials.review', 'is_approved__exact=0'),
        ('Опубліковані матеріали без презентації', StudyMaterial.objects.filter(
            no_html, is_published=True, is_bundle=False), 'materials.studymaterial',
         'is_published__exact=1&is_bundle__exact=0&has_html=no'),
        ('Неопубліковані матеріали', StudyMaterial.objects.filter(is_published=False),
         'materials.studymaterial', 'is_published__exact=0'),
        ('Завдання без теми', Question.objects.filter(curriculum_topic__isnull=True),
         'materials.question', 'curriculum_topic__isempty=1'),
    ]
    items = []
    for label, queryset, model, query in checks:
        app_label, model_name = model.split('.')
        if not request.user.has_perm(f'{app_label}.view_{model_name}'):
            continue
        items.append({'label': label, 'count': queryset.count(),
                      'url': f"{reverse(f'admin:{app_label}_{model_name}_changelist')}?{query}"})
    return items


_default_index = admin.site.index


def index_with_attention(request, extra_context=None):
    return _default_index(request, {**(extra_context or {}), 'attention_items': attention_items(request)})


admin.site.index = index_with_attention
