import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from aiogram import Bot, Dispatcher, types

from .handlers import router

dp = Dispatcher()
dp.include_router(router)


@csrf_exempt
async def telegram_webhook(request):  # Повертаємо async, Django 4+ це чудово розуміє!
    if request.method == 'POST':
        try:
            # Створюємо бота ТІЛЬКИ на час обробки повідомлення, щоб не було конфліктів у пам'яті
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

            json_data = request.body.decode('utf-8')
            update = types.Update.model_validate_json(json_data, context={"bot": bot})

            # Обробляємо повідомлення
            await dp.feed_update(bot, update)

            # Правильно закриваємо з'єднання
            await bot.session.close()

        except Exception as e:
            print(f"Помилка Webhook: {e}")

        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error", "message": "Only POST requests allowed"}, status=405)