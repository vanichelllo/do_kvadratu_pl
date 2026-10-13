import uuid

from django.contrib import admin
from django.contrib import messages
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
from .models import StudyMaterial, Category, Tag, Cart, CartItem, Order, OrderItem, DiagnosticTopic, Question, AnswerOption, MatchItem, TutorStudentRequest, Review, StudentPresentation, QuestionError, StudentReport, CurriculumSubject, CurriculumGrade, CurriculumChapter, CurriculumTopic
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
    list_filter = ('grade__subject', 'grade')
    search_fields = ('name',)
    ordering = ('grade__order', 'order')

@admin.register(CurriculumTopic)
class CurriculumTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter', 'order')
    list_filter = ('chapter__grade__subject', 'chapter__grade')
    search_fields = ('name',)
    ordering = ('chapter__order', 'order')
@admin.action(description="✅ Підтвердити статус (та видати курс для НМТ)")
def approve_student_requests(modeladmin, request, queryset):
    # Шукаємо всі матеріали НМТ
    nmt_materials = StudyMaterial.objects.filter(category__name__icontains='Підготовка до НМТ', is_published=True)

    count = 0
    for student_request in queryset.filter(status='pending'):
        # 1. Підтверджуємо заявку для всіх
        student_request.status = 'approved'
        student_request.save()

        # 2. Якщо це учень НМТ — автоматично видаємо всі матеріали НМТ
        if student_request.course == 'nmt':
            for material in nmt_materials:
                student_request.user.purchased_materials.add(material)

        count += 1

    messages.success(request, f"Успішно підтверджено заявок: {count}.")


@admin.action(description="❌ Відхилити заявки")
def reject_student_requests(modeladmin, request, queryset):
    queryset.update(status='rejected')


def materials_paid_by(user):
    """id матеріалів, за які учень заплатив сам (оплачені замовлення й архів старих покупок), разом із вмістом пакетів."""
    paid_ids = set(OrderItem.objects.filter(order__user=user, order__status='paid', material__isnull=False)
                   .values_list('material_id', flat=True))
    paid_ids |= set(PurchaseHistory.objects.filter(student=user, material__isnull=False)
                    .values_list('material_id', flat=True))
    paid_ids |= set(StudyMaterial.included_materials.through.objects.filter(from_studymaterial_id__in=paid_ids)
                    .values_list('to_studymaterial_id', flat=True))
    return paid_ids


@admin.action(description="🗑 Забрати доступ (Видалити з учнів)")
def revoke_student_access(modeladmin, request, queryset):
    # Знаходимо всі НМТ-матеріали
    nmt_materials = StudyMaterial.objects.filter(category__name__icontains='Підготовка до НМТ')

    count = 0
    kept_all = []
    for student_request in queryset:
        user = student_request.user
        # 1. Забираємо НМТ-матеріали, видані на час навчання. Куплені учнем за власні гроші
        #    і безкоштовні — залишаються (раніше зникали й вони).
        #    Якщо учень платив за матеріал, який потім видалили (наприклад, пакет), уже не видно,
        #    що в ньому було, — тоді нічого не забираємо, щоб не відібрати оплачене
        if (OrderItem.objects.filter(order__user=user, order__status='paid', material__isnull=True).exists()
                or PurchaseHistory.objects.filter(student=user, material__isnull=True).exists()):
            kept_all.append(student_request.real_name)
        else:
            keep_ids = materials_paid_by(user)
            to_remove = nmt_materials.exclude(id__in=keep_ids).exclude(is_free=True).exclude(price=0)
            user.purchased_materials.remove(*to_remove)

        # 2. Видаляємо саму заявку з бази
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
    # Якщо посилання потрапило не до тих людей — видаємо нове, а старе одразу перестає відкриватися
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
    readonly_fields = ('parent_token',) # Забороняємо редагувати токен руками
    actions = [approve_student_requests, reject_student_requests, revoke_student_access, regenerate_parent_links]

# ==========================================
# НУШ ЗВІТИ ДЛЯ БАТЬКІВ
# ==========================================
@admin.register(StudentReport)
class StudentReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'topic', 'homework_status')
    list_filter = ('date', 'homework_status', 'student__course')
    search_fields = ('student__real_name', 'topic', 'teacher_comment')

# 1. Реєструємо прості таблиці
admin.site.register(Category)
admin.site.register(Tag)


# ==========================================
# ДІАГНОСТИЧНИЙ ТЕСТ: ТЕМИ
# ==========================================
# Дію «Згенерувати діагностичний тест» прибрано: команда populate_nmt видаляла
# ВСІ завдання практики й скарги учнів. Діагностика й так бере завдання з усього банку.
@admin.register(DiagnosticTopic)
class DiagnosticTopicAdmin(admin.ModelAdmin):
    list_display = ('name',)


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
            # Лише варіанти цього завдання. Раніше кожен список містив усі ~6600 варіантів
            # з усіх завдань: сторінка важила кілька МБ і відкривалась секундами.
            # Для нового завдання варіантів ще немає — відповідність задається після збереження.
            question_id = getattr(request, '_admin_question_id', None)
            kwargs['queryset'] = (AnswerOption.objects.filter(question_id=question_id) if question_id
                                  else AnswerOption.objects.none())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic', 'question_type')
    list_select_related = ('topic',)
    list_filter = ('topic', 'question_type')
    search_fields = ('text',)
    inlines = [MatchItemInline, AnswerOptionInline]
    change_list_template = 'admin/materials/question/change_list.html'

    def get_urls(self):
        custom = [path('import-bank/', self.admin_site.admin_view(self.import_bank_view),
                       name='materials_question_import_bank')]
        return custom + super().get_urls()

    def import_bank_view(self, request):
        """Завантаження файлу bank_*.py: пробний звіт, потім імпорт."""
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
        # id завдання — на запиті (не на спільному об'єкті адмінки: його ділять потоки сервера)
        request._admin_question_id = object_id
        return super().change_view(request, object_id, form_url, extra_context)


# ==========================================
# ВІТРИНА: МАТЕРІАЛИ ТА ІМПОРТ
# ==========================================
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_published')
    list_select_related = ('category',)
    list_filter = ('is_published', 'category')
    search_fields = ('title',)
    # materials/admin.py, всередині StudyMaterialAdmin
    list_display = ('title', 'category', 'curriculum_topic', 'price', 'is_published')
    autocomplete_fields = ['curriculum_topic']  # Щоб був зручний пошук по темах НУШ
    # Дію «Імпортувати з Excel» прибрано: вона ставила всім конспектам ціну 25 грн
    # і публікувала приховані. Нові матеріали додаються тут вручну (кнопка «Додати»).


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


# === Логіка експорту Замовлень в Excel ===
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


# Кастомне поле форми для зміни формату відображення імені в списку
class ApprovedStudentChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Перевіряємо, чи є в користувача заявка (має бути, бо ми їх відфільтруємо)
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
            # 1. Фільтруємо: залишаємо лише тих, у кого заявка має статус 'approved'
            kwargs["queryset"] = User.objects.filter(tutor_request__status='approved')
            # 2. Застосовуємо наш кастомний клас для відображення "Прізвище Ім'я (email)"
            kwargs["form_class"] = ApprovedStudentChoiceField

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(QuestionError)
class QuestionErrorAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('message', 'question__text')