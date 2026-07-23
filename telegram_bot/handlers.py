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


from asgiref.sync import sync_to_async
from django.core.paginator import Paginator


# ─── ФУНКЦІЇ ДЛЯ РОБОТИ З БАЗОЮ ДАНИХ (Перекладачі) ──────────
@sync_to_async
def get_materials_page(page_number, per_page=10):
    # Беремо всі опубліковані конспекти (не пакети), сортуємо за ID
    materials = StudyMaterial.objects.filter(is_published=True, is_bundle=False).order_by('id')
    paginator = Paginator(materials, per_page)

    # Якщо сторінка виходить за межі, повертаємо порожній список
    if page_number > paginator.num_pages or page_number < 1:
        return [], paginator.num_pages

    page = paginator.page(page_number)
    return list(page.object_list), paginator.num_pages


# ─── МЕНЮ НМТ ─────────────────────────────────────────────
def get_nmt_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🎯 Перевір свій рівень (Тест)", callback_data="start_quiz")
    builder.button(text="📚 Конспекти окремих тем", callback_data="menu_materials_1")  # Починаємо з 1 сторінки
    builder.button(text="← До головного меню", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(F.data == "menu_nmt_main")
async def show_nmt_main(callback: types.CallbackQuery):
    text = "📚 <b>Підготовка до НМТ</b>\n\nТут зібрано все необхідне для твого успіху на іспиті:"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_nmt_menu_keyboard())
    await callback.answer()


# ─── КАТАЛОГ КОНСПЕКТІВ З БАЗИ ДАНИХ ───────────────────────
@router.callback_query(F.data.startswith("menu_materials_"))
async def show_materials_catalog(callback: types.CallbackQuery):
    # Витягуємо номер сторінки з callback_data (наприклад, з "menu_materials_1" дістанемо 1)
    parts = callback.data.split("_")
    current_page = int(parts[2]) if len(parts) > 2 else 1

    # Звертаємося до бази даних через нашу функцію
    materials_list, total_pages = await get_materials_page(current_page)

    if not materials_list:
        await callback.answer("Матеріалів поки немає.", show_alert=True)
        return

    builder = InlineKeyboardBuilder()

    # Генеруємо кнопки прямо з бази даних!
    for item in materials_list:
        price_text = "БЕЗКОШТОВНО" if item.is_free else f"{item.price} грн"
        # Робимо коротку назву, якщо вона занадто довга (Telegram має ліміт на довжину тексту кнопки)
        short_title = item.title[:35] + "..." if len(item.title) > 35 else item.title
        builder.button(
            text=f"📄 {short_title} — {price_text}",
            callback_data=f"info_mat_{item.id}"
        )
    builder.adjust(1)  # Кнопки в один стовпець

    # Пагінація (кнопки Вперед/Назад)
    nav_buttons = []
    if current_page > 1:
        nav_buttons.append(InlineKeyboardButton(text="← Попередня", callback_data=f"menu_materials_{current_page - 1}"))
    if current_page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text="Наступна →", callback_data=f"menu_materials_{current_page + 1}"))

    if nav_buttons:
        builder.row(*nav_buttons)

    # Кнопка назад
    builder.row(InlineKeyboardButton(text="← Назад", callback_data="menu_nmt_main"))

    text = f"<b>Конспекти окремих тем</b> (Сторінка {current_page} з {total_pages})\n\nНатискай на матеріали, щоб переглянути деталі."

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())
    await callback.answer()