from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Учень'),
        ('parent', 'Батьки / Опікун'),
        ('adult', 'Випускник / Дорослий'),
        ('teacher', 'Вчитель / Репетитор'),
    ]

    TARGET_CHOICES = [
        ('5', '5 клас'),
        ('6', '6 клас'),
        ('7', '7 клас'),
        ('8', '8 клас'),
        ('9', '9 клас'),
        ('10', '10 клас'),
        ('11', '11 клас'),
        ('nmt', 'Підготовка до НМТ / Вступ'),
        ('self', 'Для саморозвитку / Викладання'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True, verbose_name="Статус")
    target_grade = models.CharField(max_length=20, choices=TARGET_CHOICES, blank=True, null=True, verbose_name="Цільовий клас / Мета")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефону")

    balance = models.PositiveIntegerField(default=0)
    telegram_id = models.CharField(max_length=100, blank=True, null=True)
    purchased_materials = models.ManyToManyField('materials.StudyMaterial', blank=True)

    # Згода з офертою та політикою конфіденційності: коли і з якою редакцією (settings.TERMS_VERSION)
    terms_accepted_at = models.DateTimeField(null=True, blank=True, verbose_name="Згода з офертою: коли")
    # db_default: під час деплою стара версія сайту ще створює користувачів без цього поля
    terms_version = models.CharField(max_length=20, blank=True, default='', db_default='',
                                     verbose_name="Згода з офертою: редакція")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def has_accepted_current_terms(self):
        return self.terms_accepted_at is not None and self.terms_version == settings.TERMS_VERSION

    def accept_terms(self):
        self.terms_accepted_at = timezone.now()
        self.terms_version = settings.TERMS_VERSION
        self.save(update_fields=['terms_accepted_at', 'terms_version'])


class PurchaseHistory(models.Model):
    class Meta:
        verbose_name = "Покупка (архів)"
        verbose_name_plural = "Архів покупок"

    # Архів покупок старим способом (/buy/, прибрано); поточні покупки — Order/OrderItem
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='history')
    material = models.ForeignKey('materials.StudyMaterial', on_delete=models.SET_NULL, null=True)
    price_paid = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Чек: {self.student.email} | {self.price_paid} грн"