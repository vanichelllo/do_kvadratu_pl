import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from asgiref.sync import async_to_sync
from aiogram import Bot, Dispatcher, types

from .handlers import router

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


@csrf_exempt
def telegram_webhook(request):  # Зверніть увагу: прибрали слово async!
    if request.method == 'POST':
        try:
            # Читаємо дані від Telegram
            json_data = request.body.decode('utf-8')
            update = types.Update.model_validate_json(json_data, context={"bot": bot})

            # Магія: запускаємо асинхронного бота в синхронному середовищі Django
            async_to_sync(dp.feed_update)(bot, update)

        except Exception as e:
            print(f"Помилка Webhook: {e}")

        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error", "message": "Only POST requests allowed"}, status=405)