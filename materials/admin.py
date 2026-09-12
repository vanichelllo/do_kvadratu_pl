from django.contrib import admin
from django.core.management import call_command
from django.contrib import messages

# Імпорти для вивантаження бази в Excel
from import_export import resources
from import_export.admin import ExportActionMixin

from .models import StudyMaterial, Category, Tag, Cart, CartItem, Order, OrderItem, DiagnosticTopic, Question, AnswerOption, MatchItem, TutorStudentRequest, Review


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


@admin.action(description="🗑 Забрати доступ (Видалити з учнів)")
def revoke_student_access(modeladmin, request, queryset):
    # Знаходимо всі НМТ-матеріали
    nmt_materials = StudyMaterial.objects.filter(category__name__icontains='Підготовка до НМТ')

    count = 0
    for student_request in queryset:
        # 1. Забираємо в учня доступ до всіх матеріалів НМТ
        for material in nmt_materials:
            student_request.user.purchased_materials.remove(material)

        # 2. Видаляємо саму заявку з бази
        student_request.delete()
        count += 1

    messages.success(request, f"Успішно видалено {count} учнів. Доступ до матеріалів закрито.")


@admin.register(TutorStudentRequest)
class TutorStudentRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'real_name', 'course', 'status', 'created_at') # Додано 'course'
    list_filter = ('course', 'status', 'created_at') # Додано фільтр за 'course'
    search_fields = ('user__email', 'real_name')
    actions = [approve_student_requests, reject_student_requests, revoke_student_access]

# 1. Реєструємо прості таблиці
admin.site.register(Category)
admin.site.register(Tag)


# ==========================================
# ДІАГНОСТИЧНИЙ ТЕСТ: ТЕМИ ТА ГЕНЕРАЦІЯ
# ==========================================
@admin.register(DiagnosticTopic)
class DiagnosticTopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = ['populate_nmt_test']

    @admin.action(description="🔥 Згенерувати діагностичний тест НМТ (22 питання)")
    def populate_nmt_test(self, request, queryset):
        try:
            call_command('populate_nmt')
            self.message_user(request, "Успіх! Тест на 22 питання успішно згенеровано.", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Помилка генерації: {str(e)}", level=messages.ERROR)


# ==========================================
# ДІАГНОСТИЧНИЙ ТЕСТ: ПИТАННЯ ТА ВІДПОВІДІ
# ==========================================
class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 5


class MatchItemInline(admin.TabularInline):
    model = MatchItem
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic', 'question_type')
    list_filter = ('topic', 'question_type')
    search_fields = ('text',)
    inlines = [MatchItemInline, AnswerOptionInline]


# ==========================================
# ВІТРИНА: МАТЕРІАЛИ ТА ІМПОРТ
# ==========================================
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_published')
    list_filter = ('is_published', 'category')
    search_fields = ('title',)

    actions = ['import_materials_from_excel']

    @admin.action(description="🔥 Імпортувати матеріали з Excel (зшити та завантажити)")
    def import_materials_from_excel(self, request, queryset):
        try:
            call_command('import_materials')
            self.message_user(request, "Успіх! Всі матеріали імпортовано та відправлено на Cloudinary.",
                              messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Помилка імпорту: {str(e)}", level=messages.ERROR)


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
        fields = ('id', 'created_at', 'user__email', 'source', 'status', 'total_amount')
        export_order = ('id', 'created_at', 'user__email', 'source', 'status', 'total_amount')


@admin.register(Order)
class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = OrderResource

    list_display = ['id', 'user', 'total_amount', 'status', 'source', 'created_at']
    list_filter = ['status', 'source', 'created_at']
    search_fields = ['user__email', 'mono_invoice_id']
    inlines = [OrderItemInline]
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