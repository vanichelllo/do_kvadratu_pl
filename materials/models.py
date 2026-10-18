import datetime
import os
import io
import logging
import re
from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from pypdf import PdfWriter
import uuid
from django.utils import timezone

# ОНОВЛЕНО: Імпорт сховища Cloudinary
from cloudinary_storage.storage import RawMediaCloudinaryStorage


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")

    def __str__(self):
        return self.name


class Tag(models.Model):
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    name = models.CharField(max_length=50, verbose_name="Назва тегу")

    def __str__(self):
        return self.name

NMT_SUBJECT_NAME = "Підготовка до НМТ / ЗНО"
OPTION_LABEL = re.compile(r'^\s*[А-ДA-E]\)\s*')


class CurriculumSubject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Курс (напр. Алгебра 7-9)")
    order = models.PositiveIntegerField(default=0, verbose_name="Сортування")

    class Meta:
        ordering = ['order']
        verbose_name = "Курс"
        verbose_name_plural = "1. Курси"

    def __str__(self):
        return self.name

class CurriculumGrade(models.Model):
    subject = models.ForeignKey(CurriculumSubject, on_delete=models.CASCADE, related_name='grades', verbose_name="Курс")
    name = models.CharField(max_length=50, verbose_name="Клас (напр. 8 клас, НМТ)")
    number = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Номер класу (число)")
    order = models.PositiveIntegerField(default=0, verbose_name="Сортування")

    class Meta:
        ordering = ['subject__order', 'order']
        verbose_name = "Клас"
        verbose_name_plural = "2. Класи"

    def __str__(self):
        return self.short_label

    @property
    def short_label(self):
        """«Алгебра (7-9 класи)» + «8 клас» → «Алгебра · 8 клас»; для НМТ — лише «Підготовка до НМТ»."""
        if self.subject.name == NMT_SUBJECT_NAME:
            return self.name
        return f"{re.sub(r'\s*\(.*?\)', '', self.subject.name)} · {self.name}"

class CurriculumChapter(models.Model):
    grade = models.ForeignKey(CurriculumGrade, on_delete=models.CASCADE, related_name='chapters', verbose_name="Клас")
    name = models.CharField(max_length=200, verbose_name="Розділ")
    order = models.PositiveIntegerField(default=0, verbose_name="Сортування")

    class Meta:
        ordering = ['grade__subject__order', 'grade__order', 'order']
        verbose_name = "Розділ"
        verbose_name_plural = "3. Розділи"

    def __str__(self):
        return f"{self.grade.short_label} | {self.name}"

class CurriculumTopic(models.Model):
    # Узагальнення розділу — практика за всіма темами розділу; діагностика — повторення всього класу (карта прогалин)
    KIND_CHOICES = (
        ('lesson', 'Урок'),
        ('summary', 'Узагальнення розділу'),
        ('diagnostic', 'Діагностика за клас'),
    )

    chapter = models.ForeignKey(CurriculumChapter, on_delete=models.CASCADE, related_name='topics', verbose_name="Розділ")
    name = models.CharField(max_length=255, verbose_name="Тема уроку")
    order = models.PositiveIntegerField(default=0, verbose_name="Сортування")
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default='lesson', verbose_name="Тип")

    class Meta:
        ordering = ['chapter__grade__subject__order', 'chapter__grade__order', 'chapter__order', 'order']
        verbose_name = "Тема"
        verbose_name_plural = "4. Теми (Уроки)"

    def __str__(self):
        # Курс і клас на початку: розділи з однаковими назвами є в багатьох класах, і в адмінці їх легко сплутати
        return f"{self.chapter.grade.short_label} | {self.chapter.name} -> {self.name}"

DEFAULT_MATERIAL_DESCRIPTION = (
    "Авторський конспект від освітнього проєкту «До Квадрату», створений з урахуванням 7-річного досвіду "
    "викладання. Містить лише найголовніше: структуровану теорію без зайвої води, необхідні формули, алгоритми "
    "розв'язання та детальний розбір типових завдань. Підходить як для вивчення теми з нуля, так і для швидкого повторення."
)


class WithoutHtmlManager(models.Manager):
    """HTML-презентація (до кількох МБ) потрібна лише в читалці. Скрізь інде вона не
    завантажується з бази; при зверненні до material.html_content Django догрузить її окремо."""

    def get_queryset(self):
        return super().get_queryset().defer('html_content')


class StudyMaterial(models.Model):
    class Meta:
        verbose_name = "Матеріал"
        verbose_name_plural = "Матеріали"

    objects = WithoutHtmlManager()

    title = models.CharField(max_length=200, verbose_name="Назва матеріалу")
    price = models.PositiveIntegerField(default=0, verbose_name="Ціна (UAH)")

    description = models.TextField(
        verbose_name="Опис матеріалу",
        blank=True,
        null=True,
        default=DEFAULT_MATERIAL_DESCRIPTION
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

    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    curriculum_topic = models.ForeignKey(
        'CurriculumTopic', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Тема в класифікаторі (НУШ/НМТ)"
    )

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
            except Exception:
                logging.getLogger(__name__).exception("Помилка об'єднання PDF з intro.pdf")

        super().save(*args, **kwargs)

    @property
    def curriculum_grade(self):
        return self.curriculum_topic.chapter.grade if self.curriculum_topic_id else None

    @property
    def is_nmt(self):
        # Пакети й старі конспекти без теми в класифікаторі — це матеріали НМТ
        grade = self.curriculum_grade
        return grade is None or grade.subject.name == NMT_SUBJECT_NAME

    def __str__(self):
        if self.is_free:
            return f"{self.title} - БЕЗКОШТОВНО"
        return f"{self.title} - {self.price} UAH"


class Cart(models.Model):
    class Meta:
        verbose_name = "Кошик"
        verbose_name_plural = "Кошики"

    PROMO_CODE = 'ВЧИТЕЛЬ'
    PROMO_START = datetime.date(2026, 10, 2)
    PROMO_END = datetime.date(2026, 10, 11)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')

    @classmethod
    def promo_is_active(cls):
        return cls.PROMO_START <= timezone.localdate() <= cls.PROMO_END

    promo_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Промокод")
    created_at = models.DateTimeField(auto_now_add=True)

    def cached_items(self):
        """Позиції кошика з матеріалами одним запитом (ціни на сторінці рахуються кілька разів)."""
        if getattr(self, '_items_cache', None) is None:
            self._items_cache = list(self.items.select_related('material').defer('material__html_content'))
        return self._items_cache

    def get_original_price(self):
        """Рахує суму без знижки"""
        return sum(item.material.price for item in self.cached_items())

    def promo_applies(self):
        return bool(self.promo_code) and self.promo_code.upper() == self.PROMO_CODE and self.promo_is_active()

    def diagnostic_offer(self):
        """Чинна пропозиція після діагностики (знижка на уроки слабких тем), або None."""
        if not hasattr(self, '_offer_cache'):
            self._offer_cache = (DiagnosticOffer.objects.filter(user_id=self.user_id, expires_at__gt=timezone.now())
                                 .prefetch_related('materials').first())
        return self._offer_cache

    def get_offer_discount(self):
        """Знижка за діагностикою — лише на уроки з пропозиції, що лежать у кошику."""
        offer = self.diagnostic_offer()
        if not offer:
            return 0
        offer_ids = {m.id for m in offer.materials.all()}
        offer_sum = sum(item.material.price for item in self.cached_items() if item.material_id in offer_ids)
        return int(round(offer_sum * offer.discount_percent / 100))

    def get_total_price(self):
        """Фінальна сума: промокод ВЧИТЕЛЬ (−40% на все) або знижка за діагностикою — не разом, а краща з них"""
        base_price = self.get_original_price()
        if self.promo_applies():
            return int(base_price * 0.6) # Знижка 40% (множимо на 0.6)
        return base_price - self.get_offer_discount()

    def get_discount_amount(self):
        """Повертає, скільки гривень зекономив учень"""
        return self.get_original_price() - self.get_total_price()

    def __str__(self):
        return f"Кошик користувача {self.user.email}"

class DiagnosticOffer(models.Model):
    """Пропозиція на сторінці результату діагностики: уроки слабких тем зі знижкою на обмежений час.
    Нову дають не частіше, ніж раз на REPEAT_AFTER, — інакше діагностику перепроходили б заради нової знижки."""
    DISCOUNT_PERCENT = 15
    DURATION = datetime.timedelta(hours=48)
    REPEAT_AFTER = datetime.timedelta(days=30)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diagnostic_offers',
                             verbose_name="Учень")
    materials = models.ManyToManyField('StudyMaterial', related_name='diagnostic_offers', verbose_name="Уроки")
    discount_percent = models.PositiveSmallIntegerField(default=DISCOUNT_PERCENT, verbose_name="Знижка, %")
    expires_at = models.DateTimeField(verbose_name="Діє до")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Пропозиція після діагностики"
        verbose_name_plural = "Пропозиції після діагностики"

    def __str__(self):
        return f"−{self.discount_percent}% для {self.user} до {self.expires_at:%d.%m %H:%M}"

    @property
    def is_active(self):
        return self.expires_at > timezone.now()

    @classmethod
    def offer_for(cls, user, materials):
        """Чинна пропозиція користувача, або нова — якщо за REPEAT_AFTER нової ще не було."""
        now = timezone.now()
        recent = cls.objects.filter(user=user, created_at__gte=now - cls.REPEAT_AFTER).first()
        if recent:
            return recent if recent.is_active else None
        if not materials:
            return None
        offer = cls.objects.create(user=user, expires_at=now + cls.DURATION)
        offer.materials.set(materials)
        return offer


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    material = models.ForeignKey('StudyMaterial', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'material')
        verbose_name = "Товар у кошику"
        verbose_name_plural = "Товари в кошику"

    def __str__(self):
        return f"{self.material.title} у кошику"


class Order(models.Model):
    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    STATUS_CHOICES = (
        ('pending', 'Очікує оплати'),
        ('paid', 'Успішно оплачено'),
        ('cancelled', 'Скасовано'),
        ('refunded', 'Повернено (Monobank)'),
    )
    SOURCE_CHOICES = (
        ('web', 'Сайт'),
        ('bot', 'Telegram-бот'),
    )

    # Записи про оплати зберігаються й після видалення акаунта (податковий облік, політика конфіденційності,
    # розділ 8): тоді user стає порожнім, а email покупця лишається в самому замовленні
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='orders')
    customer_email = models.EmailField(blank=True, default='', db_default='', verbose_name="Email покупця")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='web', verbose_name="Джерело")
    mono_invoice_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    # Коли покупець у Кошику поставив галочку: згода з офертою і прохання відкрити матеріали
    # одразу після оплати (оферта, п. 14.1–14.2). Порожньо — у старих замовленнях і поповненнях балансу
    instant_access_agreed_at = models.DateTimeField(blank=True, null=True,
                                                    verbose_name="Галочка в Кошику (п. 14.1 оферти)")

    def save(self, *args, **kwargs):
        if not self.customer_email and self.user_id:
            self.customer_email = self.user.email
            update_fields = kwargs.get('update_fields')
            if update_fields is not None:
                kwargs['update_fields'] = list(set(update_fields) | {'customer_email'})
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Замовлення #{self.id} від {self.buyer_email} ({self.status})"

    @property
    def buyer_email(self):
        return self.customer_email or (self.user.email if self.user_id else '')


class OrderItem(models.Model):
    class Meta:
        verbose_name = "Позиція замовлення"
        verbose_name_plural = "Позиції замовлення"

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
    class Meta:
        verbose_name = "Завдання"
        verbose_name_plural = "Завдання"

    TYPE_CHOICES = (
        ('CHOICE', 'Один з п\'яти (1 бал)'),
        ('MATCH', 'Відповідність (до 3 балів)'),
        ('SHORT', 'Коротка відповідь (2 бали)'),
        # Типи лише для шкільної практики (5–11 кл.); їхні дані — у полі spec
        ('MULTI', 'Кілька правильних'),
        ('TF', 'Так / ні'),
        ('FIELDS', 'Кілька полів'),
        ('ERROR', 'Знайди помилку'),
        ('ORDER', 'Впорядкувати'),
        ('GROUP', 'Розподілити на групи'),
        ('EXPR', 'Вираз'),
        ('POINT', 'Точка на прямій'),
        ('COORD', 'Точка на площині'),
    )

    DIFFICULTY_CHOICES = (
        (1, 'Базовий (Легкий)'),
        (2, 'Стандартний (Середній)'),
        (3, 'Профільний (Складний)'),
    )


    curriculum_topic = models.ForeignKey(
        'CurriculumTopic',
        on_delete=models.SET_NULL,
        related_name='diagnostic_questions',
        null=True,
        blank=True,
        verbose_name="Тема"
    )

    materials = models.ManyToManyField('StudyMaterial', blank=True, related_name='practice_questions',
                                       verbose_name="Теги (До яких уроків належить)")
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=2, verbose_name="Складність")

    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='CHOICE', verbose_name="Тип завдання")
    text = models.TextField(verbose_name="Текст завдання")
    image = models.ImageField(upload_to='diagnostic_questions/', blank=True, null=True,
                              verbose_name="Картинка (якщо є)")

    svg_code = models.TextField(blank=True, null=True, verbose_name="SVG код малюнка (пріоритетніше за картинку)")

    correct_short_answer = models.CharField(max_length=50, blank=True, null=True,
                                            verbose_name="Відповідь (тільки для 19-22 завдань)")

    # Критерії оцінювання НУШ: у шкільній практиці (5–11 класи) за кожним учень отримує окрему оцінку 1–12
    SKILL_CHOICES = (
        ('MODEL', 'Моделювання'),
        ('SOLVE', "Розв'язування"),
        ('ANALYZE', 'Аналіз результатів'),
    )
    nush_skill = models.CharField(max_length=10, choices=SKILL_CHOICES, default='SOLVE',
                                  verbose_name="Критерій НУШ")
    hint = models.TextField(blank=True, default='', verbose_name="Підказка (показується після першої помилки, 5–6 кл.)")
    spec = models.JSONField(blank=True, default=dict,
                            verbose_name="Дані завдання (для типів шкільної практики: варіанти, кроки, групи…)")
    solution = models.TextField(blank=True, default='', verbose_name="Розв'язання (показується після відповіді)")

    def __str__(self):
        return f"[{self.get_question_type_display()}] {self.text[:40]}..."


class AnswerOption(models.Model):
    class Meta:
        verbose_name = "Варіант відповіді"
        verbose_name_plural = "Варіанти відповіді"

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255, verbose_name="Текст варіанту (напр. '5 см' або 'А')")
    is_correct = models.BooleanField(default=False, verbose_name="Це правильна відповідь? (тільки для CHOICE)")

    def __str__(self):
        return self.text

    @property
    def body(self):
        """Текст без літери «А) … Д)» на початку — літери учневі ставимо самі після перемішування."""
        return OPTION_LABEL.sub('', self.text, count=1)


class MatchItem(models.Model):
    class Meta:
        verbose_name = "Пара відповідності"
        verbose_name_plural = "Пари відповідності"

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='match_items',
                                 verbose_name="Завдання")
    text = models.CharField(max_length=255, verbose_name="Умова (ліва колонка, напр. '1. Функція парна')")
    correct_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE, verbose_name="Правильний варіант (А-Д)")

    def __str__(self):
        return f"{self.text} -> {self.correct_option.text}"


class GameMistake(models.Model):
    """Завдання, у якому учень помилився (у практиці чи іграх). Гра «Робота над помилками» дає його знову,
    доки учень не відповість правильно MASTERED_STREAK рази поспіль, — тоді запис зникає."""
    MASTERED_STREAK = 2

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='game_mistakes',
                             verbose_name="Учень")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='game_mistakes',
                                 verbose_name="Завдання")
    correct_streak = models.PositiveSmallIntegerField(default=0, verbose_name="Правильних поспіль")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Перша помилка")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Остання відповідь")

    class Meta:
        verbose_name = "Помилка учня"
        verbose_name_plural = "Помилки учнів"
        ordering = ['updated_at']
        constraints = [models.UniqueConstraint(fields=['user', 'question'], name='unique_game_mistake')]

    def __str__(self):
        return f"{self.user} — завдання #{self.question_id}"


class TutorStudentRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Очікує підтвердження'),
        ('approved', 'Підтверджено'),
        ('rejected', 'Відхилено'),
    )
    COURSE_CHOICES = (
        ('nmt', 'Підготовка до НМТ'),
        ('grade_5', 'Математика (5 клас)'),
        ('grade_6', 'Математика (6 клас)'),
        ('grade_7', 'Математика (7 клас)'),
        ('grade_8', 'Математика (8 клас)'),
        ('grade_9', 'Математика (9 клас)'),
        ('grade_10', 'Математика (10 клас)'),
        ('other', 'Закінчив/Закінчила школу'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tutor_request')
    # Викладач учня. Порожньо — учень власника сайту (заявки «Навчаєтесь у мене особисто?» і всі давніші учні)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='students', verbose_name="Викладач")
    real_name = models.CharField(max_length=100, verbose_name="Прізвище та ім'я учня")
    course = models.CharField(max_length=20, choices=COURSE_CHOICES, default='nmt', verbose_name="Напрямок / Клас")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заявки")

    # ==========================================
    # ДОДАНО: СЕКРЕТНИЙ ТОКЕН ДЛЯ БАТЬКІВ
    # ==========================================
    parent_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Токен для батьків")
    class Meta:
        verbose_name = "Заявка на статус учня"
        verbose_name_plural = "Заявки на статус учня"

    def __str__(self):
        return f"{self.real_name} ({self.get_course_display()}) - {self.get_status_display()}"


class Review(models.Model):
    RATING_CHOICES = (
        (5, '⭐⭐⭐⭐⭐ (5/5)'),
        (4, '⭐⭐⭐⭐ (4/5)'),
        (3, '⭐⭐⭐ (3/5)'),
        (2, '⭐⭐ (2/5)'),
        (1, '⭐ (1/5)'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews',
                             verbose_name="Акаунт користувача")
    # НОВЕ ПОЛЕ: Ім'я, яке введе сама людина
    reviewer_name = models.CharField(max_length=100, default="Анонім", verbose_name="Ім'я для відображення на сайті")

    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True,
                                 verbose_name="Матеріал (пусто = загальний відгук)")

    rating = models.IntegerField(choices=RATING_CHOICES, default=5, verbose_name="Оцінка")
    text = models.TextField(verbose_name="Текст відгуку")
    is_approved = models.BooleanField(default=False, verbose_name="Схвалено (показувати на сайті)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

    # Поле reviewer_name з'явилось 22.09.2026; старші відгуки отримали «Анонім» за замовчуванням
    REVIEWER_NAME_ADDED_AT = datetime.datetime(2026, 9, 22, 16, 40, tzinfo=datetime.timezone.utc)

    @property
    def display_name(self):
        """Ім'я, яке автор вписав сам. Лише для старих відгуків (до появи поля) — ім'я з профілю,
        щоб не розкривати справжнє ім'я того, хто свідомо підписався «Анонім»."""
        if self.reviewer_name == "Анонім" and self.created_at and self.created_at < self.REVIEWER_NAME_ADDED_AT:
            return self.user.first_name or "Учень"
        return self.reviewer_name or "Учень"

    def __str__(self):
        target = f"Конспект: {self.material.title}" if self.material else "Загальний відгук"
        return f"{self.reviewer_name} - {self.rating} зірок - {target}"


# ==========================================
# НОВА МОДЕЛЬ: ВІДГУКИ (REVIEWS)
# ==========================================
class PracticeAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='practice_attempts')
    material = models.ForeignKey('StudyMaterial', on_delete=models.CASCADE, related_name='attempts',
                                 verbose_name="Тема (Урок)")
    score = models.PositiveIntegerField(verbose_name="Набрано балів")
    max_score = models.PositiveIntegerField(default=18, verbose_name="Максимум балів")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата проходження")

    # НОВЕ ПОЛЕ: Зберігає всі обрані учнем варіанти
    answers_json = models.JSONField(null=True, blank=True, verbose_name="Збережені відповіді")

    # Оцінки 1–12 за критеріями НУШ — лише для шкільної практики (5–11 класи); у НМТ-практиці порожні
    nush_modeling = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Моделювання (1-12)")
    nush_solving = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Розв'язування (1-12)")
    nush_analysis = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Аналіз результатів (1-12)")
    conducted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='conducted_attempts', verbose_name="Провів на уроці (вчитель)")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Спроба проходження"
        verbose_name_plural = "Спроби проходження"

    def get_percent(self):
        return int((self.score / self.max_score) * 100) if self.max_score > 0 else 0

    @property
    def nush_grades(self):
        """[(назва критерію, оцінка або None)] — для шкільної практики; порожній список для НМТ."""
        grades = [('Моделювання', self.nush_modeling), ("Розв'язування", self.nush_solving),
                  ('Аналіз', self.nush_analysis)]
        return grades if any(g is not None for _, g in grades) else []

    def __str__(self):
        return f"{self.user.email} - {self.material.title} ({self.score}/{self.max_score})"
class PracticeRun(models.Model):
    """Незавершена шкільна практика «сходинками»: учень може піти й продовжити пізніше з того самого місця.
    Після завершення з неї створюється PracticeAttempt."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='practice_runs')
    material = models.ForeignKey('StudyMaterial', on_delete=models.CASCADE, related_name='practice_runs')
    profile = models.CharField(max_length=1, verbose_name="Профіль (A/B/C)")
    # Вчитель, який веде практику на уроці (показує екран і сам натискає): user — учень, якому вона зараховується.
    # У демонстрації без збереження user і teacher — сам вчитель
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='conducted_runs', verbose_name="Провів на уроці")
    state = models.JSONField(default=dict, verbose_name="Стан (сходинка, історія завдань)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Практика в процесі"
        verbose_name_plural = "Практики в процесі"

    def __str__(self):
        return f"{self.user} — {self.material} ({'завершено' if self.finished_at else 'в процесі'})"


class TeacherLicense(models.Model):
    """Підписка викладача на клас (напр. «Математика · 5 клас»): показ усіх уроків класу на заняттях, практика,
    ДЗ і звіти для його учнів. Учні викладача практикуються в цих темах без окремої оплати."""
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='licenses',
                                verbose_name="Викладач")
    grade = models.ForeignKey(CurriculumGrade, on_delete=models.CASCADE, related_name='licenses', verbose_name="Клас")
    valid_until = models.DateField(verbose_name="Діє до (включно)")
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=200, blank=True, verbose_name="Примітка (оплата, промо…)")

    class Meta:
        ordering = ['-valid_until']
        verbose_name = "Підписка викладача"
        verbose_name_plural = "Підписки викладачів"

    def __str__(self):
        return f"{self.teacher} — {self.grade} до {self.valid_until:%d.%m.%Y}"


class TeacherInvite(models.Model):
    """Посилання-запрошення викладача: учень відкриває його й стає учнем цього викладача."""
    teacher = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invite')
    code = models.CharField(max_length=12, unique=True)

    class Meta:
        verbose_name = "Запрошення викладача"
        verbose_name_plural = "Запрошення викладачів"

    def __str__(self):
        return f"{self.teacher}: {self.code}"


class Homework(models.Model):
    """Практика з теми, задана учневі додому до дати. Результат — перша спроба учня після видачі (attempt)."""
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='given_homeworks', verbose_name="Задав")
    student = models.ForeignKey(TutorStudentRequest, on_delete=models.CASCADE, related_name='homeworks',
                                verbose_name="Учень")
    material = models.ForeignKey('StudyMaterial', on_delete=models.CASCADE, related_name='homeworks',
                                 verbose_name="Тема (урок)")
    due_date = models.DateField(verbose_name="Виконати до")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Задано")
    attempt = models.ForeignKey(PracticeAttempt, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='homeworks', verbose_name="Результат (перша спроба після видачі)")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Домашнє завдання"
        verbose_name_plural = "Домашні завдання"

    def __str__(self):
        return f"{self.student.real_name}: {self.material.title} до {self.due_date:%d.%m.%Y}"


class StudentPresentation(models.Model):
    objects = WithoutHtmlManager()

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personal_presentations', verbose_name="Учень")
    title = models.CharField(max_length=100, verbose_name="Дата/Назва уроку (напр. 20.09.2026)")
    html_content = models.TextField(verbose_name="HTML Презентація")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Індивідуальний урок"
        verbose_name_plural = "Індивідуальні уроки"

    def __str__(self):
        return f"{self.title} — {self.student.email}"
class QuestionError(models.Model):
    STATUS_CHOICES = (
        ('new', 'Нова'),
        ('fixed', 'Виправлено'),
        ('rejected', 'Відхилено (Не помилка)'),
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='error_reports', verbose_name="Завдання")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Користувач")
    message = models.TextField(verbose_name="Опис помилки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата повідомлення")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Скарга на завдання"
        verbose_name_plural = "Скарги на завдання"

    def __str__(self):
        return f"Помилка в завданні #{self.question.id} - {self.get_status_display()}"
# ==========================================
# НОВА МОДЕЛЬ: ЗВІТИ ДЛЯ ШКОЛЯРІВ (НУШ)
# ==========================================
class StudentReport(models.Model):
    HW_CHOICES = (
        ('not_assigned', '⚪ Не задано'),
        ('not_submitted', '🔴 Не здано'),
        ('partial', '🟡 Виконано частково / з помилками'),
        ('completed', '🟢 Виконано повністю'),
    )

    student = models.ForeignKey(TutorStudentRequest, on_delete=models.CASCADE, related_name='reports', verbose_name="Учень")
    date = models.DateField(default=timezone.now, verbose_name="Дата заняття")
    # Змінено: тепер тема вибирається з нашого нового дерева
    curriculum_topic = models.ForeignKey(
        'CurriculumTopic',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Тема уроку (з програми)"
    )
    # Оцінки за критеріями НУШ (від 1 до 12)
    nush_modeling = models.PositiveIntegerField(default=0, verbose_name="Моделювання (1-12)")
    nush_solving = models.PositiveIntegerField(default=0, verbose_name="Розв'язування (1-12)")
    nush_analysis = models.PositiveIntegerField(default=0, verbose_name="Аналіз результатів (1-12)")

    homework_status = models.CharField(max_length=20, choices=HW_CHOICES, default='not_assigned', verbose_name="Домашнє завдання")
    teacher_comment = models.TextField(blank=True, verbose_name="Коментар викладача")

    class Meta:
        ordering = ['-date']
        verbose_name = "Звіт"
        verbose_name_plural = "Звіти"

    def __str__(self):
        return f"{self.date.strftime('%d.%m.%Y')} - {self.student.real_name} ({self.curriculum_topic})"