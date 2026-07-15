from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import transaction

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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def buy_material(self, material):
        if self.balance >= material.price:
            try:
                with transaction.atomic():
                    self.balance -= material.price
                    self.save()
                    self.purchased_materials.add(material)
                    PurchaseHistory.objects.create(
                        student=self,
                        material=material,
                        price_paid=material.price
                    )
                return True
            except Exception as e:
                print(f"Критична помилка при покупці: {e}")
                return False
        return False

class PurchaseHistory(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='history')
    material = models.ForeignKey('materials.StudyMaterial', on_delete=models.SET_NULL, null=True)
    price_paid = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Чек: {self.student.email} | {self.price_paid} грн"