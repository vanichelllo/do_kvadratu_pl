from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from aiogram import Bot, Dispatcher, types

# Додали імпорт нашого роутера
from .handlers import router

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Підключаємо всі команди з handlers.py до головного диспетчера
dp.include_router(router)


@csrf_exempt
async def telegram_webhook(request):
    if request.method == 'POST':
        try:
            update = types.Update.model_validate_json(
                request.body, context={"bot": bot}
            )
            await dp.feed_update(bot, update)
        except Exception as e:
            print(f"Помилка Webhook: {e}")

        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error", "message": "Only POST requests allowed"}, status=405)