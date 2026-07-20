from django.contrib import admin
from django.core.management import call_command
from django.contrib import messages
from .models import StudyMaterial, Category, Tag, Cart, CartItem, Order, OrderItem, DiagnosticTopic, Question, AnswerOption, MatchItem

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
            self.message_user(request, "Успіх! Всі матеріали імпортовано та відправлено на Cloudinary.", messages.SUCCESS)
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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'mono_invoice_id']
    inlines = [OrderItemInline]