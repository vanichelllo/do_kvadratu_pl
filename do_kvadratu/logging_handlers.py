import hashlib
import html
import logging

import requests
from django.conf import settings
from django.core.cache import cache

ALERT_COOLDOWN = 10 * 60  # однакову помилку надсилаємо не частіше разу на 10 хвилин


class TelegramErrorHandler(logging.Handler):
    """Надсилає власнику в Telegram коротке повідомлення про помилку на сайті."""

    def emit(self, record):
        try:
            token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
            chat_id = getattr(settings, 'TELEGRAM_ADMIN_ID', '')
            if not token or not chat_id:
                return

            request = getattr(record, 'request', None)
            path = getattr(request, 'path', '') if request is not None else ''
            exc_name = record.exc_info[0].__name__ if record.exc_info and record.exc_info[0] else record.levelname
            exc_text = str(record.exc_info[1])[:300] if record.exc_info and record.exc_info[1] else ''

            fingerprint = hashlib.sha256(f'{record.name}|{path}|{exc_name}|{record.lineno}'.encode()).hexdigest()
            if not cache.add(f'error-alert:{fingerprint}', 1, ALERT_COOLDOWN):
                return  # про цю помилку вже повідомляли нещодавно

            lines = ["🔥 <b>Помилка на сайті</b>"]
            if path:
                lines.append(f"Сторінка: <code>{html.escape(path)}</code>")
            lines.append(f"<b>{html.escape(exc_name)}</b>: {html.escape(exc_text or record.getMessage()[:300])}")
            lines.append("Подробиці — у логах Render.")
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                          json={'chat_id': chat_id, 'text': '\n'.join(lines), 'parse_mode': 'HTML'}, timeout=5)
        except Exception:
            # Сповіщення ніколи не повинно ламати обробку запиту
            pass
