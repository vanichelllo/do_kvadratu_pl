import logging

from allauth.account.adapter import DefaultAccountAdapter
from allauth.core import context
from django.contrib import messages

logger = logging.getLogger(__name__)


class AccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context_data):
        # Якщо Gmail відмовив (денний ліміт) або завис, раніше людина бачила сторінку помилки
        # посеред реєстрації, а повторна реєстрація казала «такий email вже існує».
        # Тепер дія завершується, а користувач бачить попередження й може повторити пізніше.
        try:
            super().send_mail(template_prefix, email, context_data)
        except Exception:
            logger.exception("Не вдалося надіслати лист (%s) на %s", template_prefix, email)
            request = context.request
            if request is not None:
                messages.warning(request, "Не вдалося надіслати лист — поштовий сервіс тимчасово недоступний. "
                                          "Спробуйте ще раз за кілька хвилин (для підтвердження пошти — "
                                          "просто увійдіть зі своїм email, і ми надішлемо лист повторно).")
