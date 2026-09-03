import os
import io
from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from pypdf import PdfWriter

# ОНОВЛЕНО: Імпорт сховища Cloudinary
from cloudinary_storage.storage import RawMediaCloudinaryStorage


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Назва тегу")

    def __str__(self):
        return self.name


class StudyMaterial(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва матеріалу")
    price = models.PositiveIntegerField(default=0, verbose_name="Ціна (UAH)")

    description = models.TextField(
        verbose_name="Опис матеріалу",
        blank=True,
        null=True,
        default="Авторський конспект від освітнього проєкту «До Квадрату» — це ваш надійний помічник для успішного складання НМТ з математики. Матеріал створений з урахуванням 7-річного досвіду викладання та містить лише найголовніше: структуровану теорію без зайвої води, усі необхідні базові формули, алгоритми розв'язання та детальний розбір типових практичних завдань. Ідеально підходить як для самостійного вивчення теми з нуля, так і для швидкого повторення перед іспитом."
    )
    image = models.ImageField(upload_to='material_images/', blank=True, null=True, verbose_name="Обкладинка (Фото)")

    file = models.FileField(
        upload_to='documents/',
        storage=RawMediaCloudinaryStorage(),
        blank=True,
        null=True,
        verbose_name="Файл матеріалу"
    )
    html_content = models.TextField(
        verbose_name="HTML Презентація",
        blank=True,
        null=True
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубліковано на вітрині")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name="Категорія")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")

    is_free = models.BooleanField(default=False, verbose_name="Безкоштовний матеріал")
    is_bundle = models.BooleanField(default=False, verbose_name="Це Пакет (Bundle)")
    included_materials = models.ManyToManyField('self', blank=True, symmetrical=False,
                                                verbose_name="Матеріали, що входять у пакет")

    def save(self, *args, **kwargs):
        is_new_file = False
        if not self.pk:
            is_new_file = True
        else:
            try:
                old_obj = type(self).objects.get(pk=self.pk)
                if old_obj.file != self.file:
                    is_new_file = True
            except type(self).DoesNotExist:
                is_new_file = True

        if is_new_file and self.file and self.file.name.lower().endswith('.pdf'):
            try:
                merger = PdfWriter()
                intro_path = os.path.join(settings.BASE_DIR, 'intro.pdf')

                if os.path.exists(intro_path):
                    merger.append(intro_path)

                merger.append(self.file.file)

                buffer = io.BytesIO()
                merger.write(buffer)
                merger.close()

                self.file.save(self.file.name, ContentFile(buffer.getvalue()), save=False)
            except Exception as e:
                print(f"Помилка об'єднання PDF: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        if self.is_free:
            return f"{self.title} - БЕЗКОШТОВНО"
        return f"{self.title} - {self.price} UAH"


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return sum(item.material.price for item in self.items.all())

    def __str__(self):
        return f"Кошик користувача {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    material = models.ForeignKey('StudyMaterial', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'material')

    def __str__(self):
        return f"{self.material.title} у кошику"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Очікує оплати'),
        ('paid', 'Успішно оплачено'),
        ('cancelled', 'Скасовано'),
    )
    SOURCE_CHOICES = (
        ('web', 'Сайт'),
        ('bot', 'Telegram-бот'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='web', verbose_name="Джерело")
    mono_invoice_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Замовлення #{self.id} від {self.user.email} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    material = models.ForeignKey('StudyMaterial', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.material.title if self.material else 'Видалений матеріал'} (Замовлення #{self.order.id})"


class DiagnosticTopic(models.Model):
    name = models.CharField(max_length=150, verbose_name="Назва теми НМТ (напр. 'Планіметрія')")
    recommended_materials = models.ManyToManyField('StudyMaterial', blank=True, verbose_name="Рекомендовані конспекти")

    def __str__(self):
        return self.name


class Question(models.Model):
    TYPE_CHOICES = (
        ('CHOICE', 'Один з п\'яти (1 бал)'),
        ('MATCH', 'Відповідність (до 3 балів)'),
        ('SHORT', 'Коротка відповідь (2 бали)'),
    )

    # Додано: Рівні складності
    DIFFICULTY_CHOICES = (
        (1, 'Базовий (Легкий)'),
        (2, 'Стандартний (Середній)'),
        (3, 'Профільний (Складний)'),
    )

    # Змінено: topic тепер може бути порожнім, бо завдання може належати тільки до практики
    topic = models.ForeignKey(DiagnosticTopic, on_delete=models.CASCADE, related_name='questions', null=True,
                              blank=True, verbose_name="Тема (для діагностики)")

    # НОВІ ПОЛЯ: Мульти-теги та складність
    materials = models.ManyToManyField('StudyMaterial', blank=True, related_name='practice_questions',
                                       verbose_name="Теги (До яких уроків належить)")
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=2, verbose_name="Складність")

    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='CHOICE', verbose_name="Тип завдання")
    text = models.TextField(verbose_name="Текст запитання")
    image = models.ImageField(upload_to='diagnostic_questions/', blank=True, null=True,
                              verbose_name="Картинка (якщо є)")

    # === НОВЕ ПОЛЕ ДЛЯ SVG ===
    svg_code = models.TextField(blank=True, null=True, verbose_name="SVG код малюнка (пріоритетніше за картинку)")

    correct_short_answer = models.CharField(max_length=50, blank=True, null=True,
                                            verbose_name="Відповідь (тільки для 19-22 завдань)")

    def __str__(self):
        return f"[{self.get_question_type_display()}] {self.text[:40]}..."


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255, verbose_name="Текст варіанту (напр. '5 см' або 'А')")
    is_correct = models.BooleanField(default=False, verbose_name="Це правильна відповідь? (тільки для CHOICE)")

    def __str__(self):
        return self.text


class MatchItem(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='match_items',
                                 verbose_name="Завдання")
    text = models.CharField(max_length=255, verbose_name="Умова (ліва колонка, напр. '1. Функція парна')")
    correct_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE, verbose_name="Правильний варіант (А-Д)")

    def __str__(self):
        return f"{self.text} -> {self.correct_option.text}"


# ==========================================
# НОВА МОДЕЛЬ: ІСТОРІЯ ПРОХОДЖЕННЯ ПРАКТИКИ
# ==========================================
class PracticeAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='practice_attempts')
    material = models.ForeignKey('StudyMaterial', on_delete=models.CASCADE, related_name='attempts',
                                 verbose_name="Тема (Урок)")
    score = models.PositiveIntegerField(verbose_name="Набрано балів")
    max_score = models.PositiveIntegerField(default=18, verbose_name="Максимум балів")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата проходження")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Спроба проходження"
        verbose_name_plural = "Спроби проходження"

    def get_percent(self):
        return int((self.score / self.max_score) * 100) if self.max_score > 0 else 0

    def __str__(self):
        return f"{self.user.email} - {self.material.title} ({self.score}/{self.max_score})"