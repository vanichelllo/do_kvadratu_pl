import uuid
import datetime
from django.contrib import admin
from django.contrib import messages
from django.db.models import BooleanField, Case, Q, Value, When
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import path

# Імпорти для вивантаження бази в Excel
from import_export import resources
from import_export.admin import ExportActionMixin
from django import forms
from django.contrib.auth import get_user_model

from users.models import PurchaseHistory
from .bank_import import MAX_FILE_BYTES, BankFormatError, build_report, import_tasks, parse_bank_source
from .models import (
    StudyMaterial, Tag, Cart, CartItem, Order, OrderItem,
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


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # ОНОВЛЕНО: curriculum_topic замість topic
    list_display = ('text', 'curriculum_topic', 'question_type')
    list_select_related = ('curriculum_topic__chapter__grade__subject',)
    # Фільтр за класом, а не за кожною з сотень тем; окремо — завдання без теми
    list_filter = ('curriculum_topic__chapter__grade', ('curriculum_topic', admin.EmptyFieldListFilter),
                   'question_type', 'difficulty')
    search_fields = ('text',)
    autocomplete_fields = ['curriculum_topic']
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


class StudyMaterialAdmin(admin.ModelAdmin):
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
    list_display = ('question', 'user', 'status', 'created_at')
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
