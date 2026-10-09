import hmac
import json
import logging
import asyncio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from aiogram import Bot, Dispatcher, types

from .handlers import router
from .storage import DjangoStorage

logger = logging.getLogger(__name__)

# Стани діалогів — у базі даних (раніше в пам'яті: губились після перезапуску сервера)
dp = Dispatcher(storage=DjangoStorage())
dp.include_router(router)


@csrf_exempt
def telegram_webhook(request):  # Зверніть увагу, це знову звичайний def (без async)
    # Telegram надсилає secret_token, вказаний у setWebhook, у цьому заголовку.
    # Без перевірки будь-хто міг підробити оновлення (зокрема /send від імені адміна).
    webhook_secret = getattr(settings, 'TELEGRAM_WEBHOOK_SECRET', '') or ''
    if webhook_secret:
        provided_secret = request.headers.get('X-Telegram-Bot-Api-Secret-Token', '')
        if not hmac.compare_digest(provided_secret, webhook_secret):
            return JsonResponse({"status": "forbidden"}, status=403)

    if request.method == 'POST':
        try:
            json_data = request.body.decode('utf-8')

            # Ізольована функція для безпечного запуску асинхронного коду
            def process_update():
                # Створюємо новий чистий потік (event loop) спеціально для цього запиту
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
                # Парсимо повідомлення від Telegram
                update = types.Update.model_validate_json(json_data, context={"bot": bot})

                try:
                    # Згодовуємо повідомлення боту
                    loop.run_until_complete(dp.feed_update(bot, update))
                except Exception:
                    logger.exception("Помилка всередині бота")
                finally:
                    # Чистимо пам'ять і закриваємо з'єднання
                    loop.run_until_complete(bot.session.close())
                    loop.close()

            # Запускаємо нашу функцію
            process_update()

        except Exception:
            logger.exception("Помилка вебхука Telegram")

        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error", "message": "Only POST requests allowed"}, status=405)