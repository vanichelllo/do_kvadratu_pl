from django.contrib import admin
from .models import CustomUser, PurchaseHistory

admin.site.register(CustomUser)
# Реєструємо історію покупок для аудиту
admin.site.register(PurchaseHistory)