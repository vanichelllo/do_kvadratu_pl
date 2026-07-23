import json
import asyncio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from aiogram import Bot, Dispatcher, types

from .handlers import router

dp = Dispatcher()
dp.include_router(router)


@csrf_exempt
def telegram_webhook(request):  # Зверніть увагу, це знову звичайний def (без async)
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
                except Exception as e:
                    print(f"Помилка всередині бота: {e}")
                finally:
                    # Чистимо пам'ять і закриваємо з'єднання
                    loop.run_until_complete(bot.session.close())
                    loop.close()

            # Запускаємо нашу функцію
            process_update()

        except Exception as e:
            print(f"Помилка Webhook: {e}")

        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error", "message": "Only POST requests allowed"}, status=405)