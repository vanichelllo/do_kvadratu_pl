from django.db import models


class BotFSMState(models.Model):
    """Стан діалогу з ботом (квіз, анкета, підтримка). Раніше зберігався в пам'яті процесу
    і губився після кожного перезапуску сервера."""
    key = models.CharField(max_length=255, unique=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    data = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key}: {self.state or '—'}"


class BotCachedFile(models.Model):
    """file_id уже надісланого в Telegram файлу (напр. «Вся база для НМТ»), щоб не склеювати його щоразу."""
    key = models.CharField(max_length=255, unique=True)
    file_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key


class BotLead(models.Model):
    """Заявка на заняття з анкети в боті."""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    telegram_id = models.BigIntegerField(verbose_name="Telegram ID")
    telegram_username = models.CharField(max_length=100, blank=True, verbose_name="Нікнейм у Telegram")
    telegram_name = models.CharField(max_length=255, blank=True, verbose_name="Ім'я в Telegram")
    role = models.CharField(max_length=50, blank=True, verbose_name="Хто заповнив")
    subject = models.CharField(max_length=100, blank=True, verbose_name="Категорія")
    name = models.CharField(max_length=255, blank=True, verbose_name="Ім'я учня")
    grade = models.CharField(max_length=100, blank=True, verbose_name="Клас")
    goal = models.TextField(blank=True, verbose_name="Мета")
    contact = models.CharField(max_length=255, blank=True, verbose_name="Контакт")
    processed = models.BooleanField(default=False, verbose_name="Опрацьовано")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Заявка з бота"
        verbose_name_plural = "Заявки з бота"

    def __str__(self):
        return f"{self.name or self.telegram_name} ({self.contact}) — {self.created_at:%d.%m.%Y}"
