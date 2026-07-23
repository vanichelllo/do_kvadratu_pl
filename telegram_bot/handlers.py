from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async

# ОП! Магія: тепер ми маємо прямий доступ до бази даних сайту!
from materials.models import StudyMaterial
from django.contrib.auth import get_user_model

User = get_user_model()
router = Router()

BOT_NAME = "do_kvadratu"
CONTACT = "@do_kvadratu"

# ─── Клавіатури ──────────────────────────────────────────────────────────────
def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🎓 Підготовка до НМТ", callback_data="menu_nmt_main")
    builder.button(text="🎒 Заняття (5-10 класи)", callback_data="menu_5_10")
    builder.button(text="🎯 Інші навчальні потреби", callback_data="menu_other")
    builder.button(text="👨‍🏫 Про мене", callback_data="menu_about")
    builder.button(text="📱 Соцмережі", callback_data="menu_socials")
    builder.adjust(1)
    return builder.as_markup()

# ─── Головне меню ────────────────────────────────────────────────────────────
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        f"Вітаю! Це бот проєкту <b>{BOT_NAME}</b>\n\n"
        f"Твій головний помічник у вивченні математики та підготовці до іспитів.\n"
        f"Обери потрібний розділ нижче:"
    )
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=get_main_menu_keyboard())

@router.callback_query(F.data == "back_main")
async def back_to_main(callback: types.CallbackQuery):
    menu_text = f"Ти у головному меню проєкту <b>{BOT_NAME}</b>\n\nОбери розділ:"
    if callback.message.document or callback.message.photo:
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass
        await callback.message.answer(menu_text, parse_mode="HTML", reply_markup=get_main_menu_keyboard())
    else:
        await callback.message.edit_text(menu_text, parse_mode="HTML", reply_markup=get_main_menu_keyboard())
    await callback.answer()

@router.callback_query(F.data == "menu_about")
async def show_about(callback: types.CallbackQuery):
    text = (
        "👨‍🏫 <b>Про мене</b>\n\n"
        "Привіт! Я — Іван, професійний викладач математики із 7-річним досвідом. "
        "У 2024–2025 роках я працював вчителем математики, а зараз продовжую роботу в державній школі, "
        "тому чудово бачу систему освіти зсередини. Я знаю всі «підводні камені» шкільної програми, "
        "реальні вимоги до іспитів та найчастіші помилки учнів.\n\n"
        "📈 <b>Математика на практиці:</b>\n"
        "Для мене це не лише суха теорія. Я маю реальний досвід застосування математики у великому бізнесі. "
        "Працюючи менеджером з асортименту в мережі супермаркетів, я щодня використовував математичні моделі, "
        "проводив ABC/XYZ-аналіз та працював з великими масивами даних (Power BI)."
    )
    builder = InlineKeyboardBuilder()
    builder.button(text="← До головного меню", callback_data="back_main")
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())
    await callback.answer()