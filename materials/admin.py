from django.contrib import admin
from .models import StudyMaterial, Category, Tag, Cart, CartItem, Order, OrderItem, DiagnosticTopic, Question, AnswerOption # Додали імпорт Category

# 1. Реєструємо таблицю категорій (найпростіший варіант без додаткових налаштувань)
admin.site.register(Category)
admin.site.register(Tag)
# Реєструємо теми, щоб ви могли їх додавати та прив'язувати конспекти
admin.site.register(DiagnosticTopic)


# Налаштовуємо зручне відображення варіантів відповідей прямо всередині питання
class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 5  # Одразу виводимо 5 порожніх полів для А, Б, В, Г, Д


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic', 'question_type')  # Що показувати в списку питань
    list_filter = ('topic', 'question_type')  # Фільтри збоку для зручності
    search_fields = ('text',)  # Пошук по тексту питання
    inlines = [AnswerOptionInline]  # Підключаємо варіанти відповідей знизу
# 2. Оновлюємо налаштування матеріалів
class StudyMaterialAdmin(admin.ModelAdmin):
    # Додали 'category' у відображення колонок
    list_display = ('title', 'category', 'price', 'is_published')

    # Додали 'category' у бічний фільтр
    list_filter = ('is_published', 'category')

    search_fields = ('title',)


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