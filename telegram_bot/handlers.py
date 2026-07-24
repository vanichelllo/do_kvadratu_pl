import io
import aiohttp
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BufferedInputFile

from asgiref.sync import sync_to_async
from materials.models import StudyMaterial
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.conf import settings
from datetime import datetime

User = get_user_model()
router = Router()

BOT_NAME = "do_kvadratu"
CONTACT = "@do_kvadratu"

# Тимчасова пам'ять
user_carts = {}
pending_orders = {}


# ─── ФУНКЦІЇ ДЛЯ РОБОТИ З БАЗОЮ ДАНИХ ТА PDF ─────────────────
@sync_to_async
def get_materials_page(page_number, per_page=10, is_bundle=False):
    materials = StudyMaterial.objects.filter(is_published=True, is_bundle=is_bundle).order_by('id')
    paginator = Paginator(materials, per_page)

    if page_number > paginator.num_pages or page_number < 1:
        return [], paginator.num_pages

    page = paginator.page(page_number)
    return list(page.object_list), paginator.num_pages


@sync_to_async
def get_cart_details(item_ids):
    materials = StudyMaterial.objects.filter(id__in=item_ids)
    total_price = sum(item.price for item in materials if not item.is_free)
    titles = [item.title for item in materials]
    return total_price, titles


@sync_to_async
def get_materials_by_ids(item_ids):
    return list(StudyMaterial.objects.filter(id__in=item_ids))


@sync_to_async
def get_free_materials_urls():
    materials = StudyMaterial.objects.filter(is_published=True, is_free=True).order_by('id')
    return [mat.file.url for mat in materials if mat.file]


async def merge_and_watermark(pdf_urls: list, user_id: int) -> bytes:
    # 1. Створюємо водяний знак (один раз для всіх сторінок)
    watermark_buffer = io.BytesIO()
    c = canvas.Canvas(watermark_buffer, pagesize=A4)
    c.setFillColor(Color(0.5, 0.5, 0.5, alpha=0.2))
    c.setFont("Helvetica-Bold", 36)
    c.translate(300, 400)
    c.rotate(45)
    c.drawCentredString(0, 0, f"DO KVADRATU | USER ID: {user_id}")
    c.save()

    watermark_buffer.seek(0)
    watermark_page = PdfReader(watermark_buffer).pages[0]

    # 2. Завантажуємо, маркуємо та зшиваємо ВСІ обрані файли
    writer = PdfWriter()
    async with aiohttp.ClientSession() as session:
        for url in pdf_urls:
            if url.startswith("http://"):
                url = url.replace("http://", "https://")

            async with session.get(url) as resp:
                if resp.status == 200:
                    pdf_bytes = await resp.read()
                    reader = PdfReader(io.BytesIO(pdf_bytes))
                    for page in reader.pages:
                        page.merge_page(watermark_page)
                        writer.add_page(page)

    # 3. Зберігаємо фінальний склеєний результат
    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer.read()


# ─── КЛАВІАТУРИ ──────────────────────────────────────────────
def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🎓 Підготовка до НМТ", callback_data="menu_nmt_main")
    builder.button(text="🎒 Заняття (5-10 класи)", callback_data="menu_5_10")
    builder.button(text="🎯 Інші навчальні потреби", callback_data="menu_other")
    builder.button(text="👨‍🏫 Про мене", callback_data="menu_about")
    builder.button(text="📱 Соцмережі", callback_data="menu_socials")
    builder.adjust(1)
    return builder.as_markup()


def get_nmt_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🎯 Перевір свій рівень (Тест)", callback_data="start_quiz")
    builder.button(text="📚 Окремі теми", callback_data="menu_materials_1")
    builder.button(text="📦 Готові пакети", callback_data="menu_bundles_1")
    builder.button(text="🎁 Вся база для НМТ (1 файлом)", callback_data="download_all_free")
    builder.button(text="← До головного меню", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()


# ─── ГОЛОВНЕ МЕНЮ ТА ІНФО ────────────────────────────────────
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
        "У 2024–2025 роках я працював вчителем математики, а зараз продовжую роботу в державній школі..."
    )
    builder = InlineKeyboardBuilder()
    builder.button(text="← До головного меню", callback_data="back_main")
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "menu_socials")
async def show_socials(callback: types.CallbackQuery):
    text = (
        "📱 <b>Мої соцмережі</b>\n\n"
        "Підписуйся, щоб отримувати розбори складних задач та лайфхаки для НМТ!\n\n"
        f"Зв'язок зі мною: {CONTACT}"
    )
    builder = InlineKeyboardBuilder()
    builder.button(text="Instagram", url="https://instagram.com/do_kvadratu")
    builder.button(text="Telegram-канал", url="https://t.me/do_kvadratu")
    builder.button(text="← До головного меню", callback_data="back_main")
    builder.adjust(1)
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "menu_nmt_main")
async def show_nmt_main(callback: types.CallbackQuery):
    text = "📚 <b>Підготовка до НМТ</b>\n\nТут зібрано все необхідне для твого успіху на іспиті:"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_nmt_menu_keyboard())
    await callback.answer()


# ─── ЛОГІКА ВІДОБРАЖЕННЯ ТА КОШИКА ──────────────────────────
async def render_materials_page(callback: types.CallbackQuery, page: int, is_bundle: bool):
    user_id = callback.from_user.id
    if user_id not in user_carts:
        user_carts[user_id] = set()

    materials_list, total_pages = await get_materials_page(page, is_bundle=is_bundle)

    if not materials_list:
        await callback.answer("Матеріалів поки немає.", show_alert=True)
        return

    builder = InlineKeyboardBuilder()
    cb_prefix = "bundle" if is_bundle else "single"

    for item in materials_list:
        price_text = "БЕЗКОШТОВНО" if item.is_free else f"{item.price} грн"
        mark = "✅ " if item.id in user_carts[user_id] else ("📦 " if is_bundle else "📄 ")
        short_title = item.title[:30] + "..." if len(item.title) > 30 else item.title

        builder.button(
            text=f"{mark}{short_title} — {price_text}",
            callback_data=f"toggle_mat_{item.id}_{page}_{cb_prefix}"
        )
    builder.adjust(1)

    nav_buttons = []
    nav_cb = "menu_bundles_" if is_bundle else "menu_materials_"
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="← Попередня", callback_data=f"{nav_cb}{page - 1}"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text="Наступна →", callback_data=f"{nav_cb}{page + 1}"))
    if nav_buttons:
        builder.row(*nav_buttons)

    if user_carts[user_id]:
        builder.row(InlineKeyboardButton(text=f"🛒 Отримати обрані ({len(user_carts[user_id])} шт.)",
                                         callback_data="checkout_cart"))

    builder.row(InlineKeyboardButton(text="← Назад", callback_data="menu_nmt_main"))

    title_str = "Готові пакети" if is_bundle else "Конспекти окремих тем"
    text = f"<b>{title_str}</b> (Сторінка {page} з {total_pages})\n\nНатискай на матеріали, щоб додати їх до збірки."
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("menu_materials_"))
async def show_materials_catalog(callback: types.CallbackQuery):
    try:
        parts = callback.data.split("_")
        current_page = int(parts[2]) if len(parts) > 2 else 1
        await render_materials_page(callback, current_page, is_bundle=False)
        await callback.answer()
    except Exception as e:
        await callback.answer("Помилка завантаження.", show_alert=True)


@router.callback_query(F.data.startswith("menu_bundles_"))
async def show_bundles_catalog(callback: types.CallbackQuery):
    try:
        parts = callback.data.split("_")
        current_page = int(parts[2]) if len(parts) > 2 else 1
        await render_materials_page(callback, current_page, is_bundle=True)
        await callback.answer()
    except Exception as e:
        await callback.answer("Помилка завантаження.", show_alert=True)


@router.callback_query(F.data.startswith("toggle_mat_"))
async def toggle_material(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    item_id = int(parts[2])
    page = int(parts[3])
    is_bundle = (parts[4] == "bundle")
    user_id = callback.from_user.id

    if user_id not in user_carts:
        user_carts[user_id] = set()

    if item_id in user_carts[user_id]:
        user_carts[user_id].remove(item_id)
    else:
        user_carts[user_id].add(item_id)

    await render_materials_page(callback, page, is_bundle)
    await callback.answer()


@router.callback_query(F.data == "download_all_free")
async def send_all_free_materials(callback: types.CallbackQuery):
    await callback.answer()

    wait_msg = await callback.message.answer(
        "⏳ <i>Завантажую та зшиваю збірку «Вся база для НМТ». Це може зайняти близько хвилини...</i>",
        parse_mode="HTML"
    )

    try:
        urls = await get_free_materials_urls()
        if not urls:
            await wait_msg.edit_text("На жаль, матеріалів для бази поки немає.")
            return

        writer = PdfWriter()
        async with aiohttp.ClientSession() as session:
            for url in urls:
                if url.startswith("http://"):
                    url = url.replace("http://", "https://")
                async with session.get(url) as resp:
                    if resp.status == 200:
                        pdf_bytes = await resp.read()
                        reader = PdfReader(io.BytesIO(pdf_bytes))
                        for page in reader.pages:
                            writer.add_page(page)

        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)

        await callback.message.answer_document(
            document=BufferedInputFile(output_buffer.read(), filename="Вся_база_для_НМТ.pdf"),
            caption="🎁 Тримай велику збірку «Вся база для НМТ»! Успішної підготовки."
        )
        await wait_msg.delete()

    except Exception as e:
        print(f"Помилка зшивання: {e}")
        await wait_msg.edit_text("❌ Сталася помилка при формуванні файлу.")


# ─── ОФОРМЛЕННЯ ЗАМОВЛЕННЯ ──────────────────────────────────
@router.callback_query(F.data == "checkout_cart")
async def process_checkout(callback: types.CallbackQuery):
    user = callback.from_user
    if user.id not in user_carts or not user_carts[user.id]:
        await callback.answer("Ваш кошик порожній!", show_alert=True)
        return

    item_ids = list(user_carts[user.id])
    total_price, titles = await get_cart_details(item_ids)

    title_text = f"Збірка конспектів ({len(item_ids)} шт.)"
    builder = InlineKeyboardBuilder()

    pending_orders[user.id] = {
        "username": user.full_name,
        "items": item_ids,
        "title": title_text,
        "price": total_price,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        admin_id = int(settings.TELEGRAM_ADMIN_ID)
        await callback.bot.send_message(
            admin_id,
            f"<b>Нове замовлення (Кошик)</b>\n\n"
            f"Учень: {user.full_name}\n"
            f"ID: <code>{user.id}</code>\n"
            f"Сума: {total_price} грн\n\n"
            f"Очікуємо підтвердження оплати...",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Помилка відправки адміну: {e}")

    # ВСТАВТЕ СВІЙ НОМЕР КАРТКИ ТУТ 👇
    card_number = "1234 5678 1234 5678"

    builder.button(text="Я оплатив(ла)", callback_data="paid_confirm")
    builder.button(text="← Назад", callback_data="menu_materials_1")
    builder.adjust(1)

    await callback.message.edit_text(
        f"<b>Оплата замовлення</b>\n\n"
        f"Товар: {title_text}\n"
        f"Сума до сплати: <b>{total_price} грн</b>\n\n"
        f"1. Перекажи кошти на картку (натисни, щоб скопіювати):\n<code>{card_number}</code>\n\n"
        f"2. Після оплати обов'язково натисни кнопку нижче.",
        parse_mode="HTML",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


# ─── ПІДТВЕРДЖЕННЯ ОПЛАТИ ──────────────────────────────────
@router.callback_query(F.data == "paid_confirm")
async def paid_confirm(callback: types.CallbackQuery):
    user = callback.from_user
    order = pending_orders.get(user.id)

    if not order:
        await callback.answer("Замовлення не знайдено.", show_alert=True)
        return

    try:
        admin_id = int(settings.TELEGRAM_ADMIN_ID)
        await callback.bot.send_message(
            admin_id,
            f"💸 <b>{user.full_name}</b> підтвердив(ла) оплату!\n\n"
            f"ID: <code>{user.id}</code>\n"
            f"Очікувана сума: <b>{order['price']} грн</b>\n\n"
            f"Щоб підтвердити замовлення і видати матеріали, надішли команду:\n<code>/approve {user.id}</code>",
            parse_mode="HTML"
        )
    except Exception:
        pass

    builder = InlineKeyboardBuilder()
    builder.button(text="← До меню НМТ", callback_data="menu_nmt_main")

    await callback.message.edit_text(
        "Дякую! Твоє повідомлення отримано.\n"
        "Я перевірю надходження коштів і надішлю матеріали сюди.\n\n"
        f"Якщо є питання, пиши: {CONTACT}",
        parse_mode="HTML", reply_markup=builder.as_markup()
    )
    await callback.answer()


# ─── АДМІНСЬКА КОМАНДА ВІДПРАВКИ ────────────────────────────
@router.message(Command("approve"))
async def approve_order(message: types.Message):
    try:
        admin_id = int(settings.TELEGRAM_ADMIN_ID)
    except Exception:
        return

    if message.from_user.id != admin_id:
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.reply("Використання: <code>/approve ID_користувача</code>", parse_mode="HTML")
        return

    user_id = int(parts[1])
    order = pending_orders.get(user_id)

    if not order:
        await message.reply(f"Активних замовлень для ID {user_id} не знайдено.")
        return

    await message.reply(
        "⏳ <i>Генерую водяні знаки, зшиваю файли та завантажую матеріали... Це може зайняти до хвилини.</i>",
        parse_mode="HTML")

    try:
        # Беремо матеріали з бази
        materials = await get_materials_by_ids(order["items"])
        urls = [mat.file.url for mat in materials if mat.file]

        if not urls:
            await message.reply("Помилка: у цих матеріалах відсутні файли!")
            return

        # Сповіщаємо учня про успіх
        await message.bot.send_message(
            user_id,
            "<b>Оплата успішна!</b> 🎉\n\nТвоє замовлення готове. Бажаю ефективної підготовки!",
            parse_mode="HTML"
        )

        # МАКІЯ: Всі файли з кошика зшиваються в один PDF і отримують водяний знак
        watermarked_pdf = await merge_and_watermark(urls, user_id)

        # Визначаємо гарну назву файлу (якщо товар був один - беремо його назву, якщо декілька - називаємо збіркою)
        if len(materials) == 1:
            filename = f"{materials[0].title}.pdf"
        else:
            filename = "Персональна_збірка_конспектів.pdf"

        # Відправляємо фінальний єдиний файл
        await message.bot.send_document(
            user_id,
            document=BufferedInputFile(watermarked_pdf, filename=filename),
            caption="📄 Твої матеріали\n\n🔒 <i>Файл персоналізовано та захищено авторським правом. Пересилання заборонено.</i>",
            protect_content=True  # Додав захист від пересилання в Telegram
        )

        # Очищуємо пам'ять
        if user_id in user_carts:
            user_carts[user_id].clear()
        del pending_orders[user_id]

        await message.reply(f"✅ Замовлення завершено! Персоналізований файл надіслано учню {user_id}.")
    except Exception as e:
        await message.reply(f"Помилка при відправці файлів: {e}")
        print(f"Помилка відправки: {e}")