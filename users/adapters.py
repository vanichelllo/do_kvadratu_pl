import logging

from allauth.account.adapter import DefaultAccountAdapter

logger = logging.getLogger(__name__)


class AccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        # Якщо Gmail відмовив (денний ліміт) або завис, раніше людина бачила сторінку помилки
        # посеред реєстрації, а повторна реєстрація казала «такий email вже існує».
        # Тепер реєстрація завершується; лист можна надіслати повторно зі сторінки входу.
        try:
            super().send_mail(template_prefix, email, context)
        except Exception:
            logger.exception("Не вдалося надіслати лист (%s) на %s", template_prefix, email)
