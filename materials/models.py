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

    # ОНОВЛЕНО: Намертво прив'язуємо це поле до хмари Cloudinary
    file = models.FileField(
        upload_to='documents/',
        storage=RawMediaCloudinaryStorage(),
        blank=True,
        null=True,
        verbose_name="Файл матеріалу"
    )

    is_published = models.BooleanField(default=False, verbose_name="Опубліковано на вітрині")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name="Категорія")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")

    is_free = models.BooleanField(default=False, verbose_name="Безкоштовний матеріал")
    is_bundle = models.BooleanField(default=False, verbose_name="Це Пакет (Bundle)")
    included_materials = models.ManyToManyField('self', blank=True, symmetrical=False,
                                                verbose_name="Матеріали, що входять у пакет")

    def save(self, *args, **kwargs):
        # Перевіряємо, чи це нове завантаження файлу
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

        # Якщо завантажено новий PDF-файл (перевіряємо поле self.file)
        if is_new_file and self.file and self.file.name.lower().endswith('.pdf'):
            try:
                merger = PdfWriter()

                # 1. Знаходимо intro.pdf у корені проєкту
                intro_path = os.path.join(settings.BASE_DIR, 'intro.pdf')

                # Якщо файл інтро існує, ставимо його першим
                if os.path.exists(intro_path):
                    merger.append(intro_path)

                # 2. Додаємо сам матеріал
                merger.append(self.file.file)

                # 3. Зберігаємо результат у віртуальну пам'ять
                buffer = io.BytesIO()
                merger.write(buffer)
                merger.close()

                # 4. Підміняємо оригінальний файл на об'єднаний
                self.file.save(self.file.name, ContentFile(buffer.getvalue()), save=False)
            except Exception as e:
                print(f"Помилка об'єднання PDF: {e}")

        # Зберігаємо модель у базу даних
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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
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
    # Оновлено назви для зручності в адмінці
    TYPE_CHOICES = (
        ('CHOICE', 'Один з п\'яти (1 бал)'),
        ('MATCH', 'Відповідність (до 3 балів)'),
        ('SHORT', 'Коротка відповідь (2 бали)'),
    )

    topic = models.ForeignKey(DiagnosticTopic, on_delete=models.CASCADE, related_name='questions', verbose_name="Тема")
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='CHOICE', verbose_name="Тип завдання")
    text = models.TextField(verbose_name="Текст запитання")
    image = models.ImageField(upload_to='diagnostic_questions/', blank=True, null=True,
                              verbose_name="Картинка (якщо є)")
    correct_short_answer = models.CharField(max_length=50, blank=True, null=True,
                                            verbose_name="Відповідь (тільки для 19-22 завдань)")

    def __str__(self):
        return f"[{self.get_question_type_display()}] {self.text[:40]}..."


class AnswerOption(models.Model):
    """
    Працює для CHOICE як варіанти відповідей (з позначкою is_correct).
    Працює для MATCH як права колонка (А, Б, В, Г, Д) - тут is_correct не враховується.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255, verbose_name="Текст варіанту (напр. '5 см' або 'А')")
    is_correct = models.BooleanField(default=False, verbose_name="Це правильна відповідь? (тільки для CHOICE)")

    def __str__(self):
        return self.text


# ==========================================
# НОВА МОДЕЛЬ: ЛІВА ЧАСТИНА ВІДПОВІДНОСТІ
# ==========================================
class MatchItem(models.Model):
    """Ліва частина завдання на відповідність (цифри 1, 2, 3)"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='match_items',
                                 verbose_name="Завдання")
    text = models.CharField(max_length=255, verbose_name="Умова (ліва колонка, напр. '1. Функція парна')")
    # Зв'язуємо кожну цифру (1-3) з правильною буквою (А-Д) з таблиці AnswerOption
    correct_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE, verbose_name="Правильний варіант (А-Д)")

    def __str__(self):
        return f"{self.text} -> {self.correct_option.text}"