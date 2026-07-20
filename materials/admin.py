from django.contrib import admin
from django.core.management import call_command
from django.contrib import messages
from .models import StudyMaterial, Category, Tag, Cart, CartItem, Order, OrderItem, DiagnosticTopic, Question, \
    AnswerOption

# 1. Реєструємо таблицю категорій
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(DiagnosticTopic)


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 5


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic', 'question_type')
    list_filter = ('topic', 'question_type')
    search_fields = ('text',)
    inlines = [AnswerOptionInline]


# 2. Оновлюємо налаштування матеріалів
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_published')
    list_filter = ('is_published', 'category')
    search_fields = ('title',)

    # ДОДАЄМО НАШУ КНОПКУ ІМПОРТУ
    actions = ['import_materials_from_excel']

    @admin.action(description="🔥 Імпортувати матеріали з Excel (зшити та завантажити)")
    def import_materials_from_excel(self, request, queryset):
        try:
            # Запускаємо скрипт імпорту, який ми раніше створили
            call_command('import_materials')
            self.message_user(request, "Успіх! Всі матеріали імпортовано та відправлено на Cloudinary.",
                              messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Помилка імпорту: {str(e)}", level=messages.ERROR)


admin.site.register(StudyMaterial, StudyMaterialAdmin)


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