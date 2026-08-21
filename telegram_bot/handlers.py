import io
import aiohttp
from pypdf import PdfReader, PdfWriter

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BufferedInputFile, WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from asgiref.sync import sync_to_async

from materials.models import StudyMaterial
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()
router = Router()

BOT_NAME = "do_kvadratu"
CONTACT = "@do_kvadratu"


# ─── СТАНИ FSM ───────────────────────────────────────────────
class QuizFSM(StatesGroup):
    answering_choice = State()
    answering_short = State()


class EnrollFSM(StatesGroup):
    role = State()
    name = State()
    grade = State()
    goal = State()
    phone = State()


class SupportFSM(StatesGroup):
    waiting_for_question = State()


# ─── ЗАПИТАННЯ ДІАГНОСТИЧНОГО ТЕСТУ ──────────────────────────
DIAGNOSTIC_QUESTIONS = [
    {"q": "<b>1/22.</b> Розв’яжіть рівняння: 3x / 4 = 6.", "t": "6. Лінійні рівняння. Лінійні рівняння з параметром",
     "type": "choice", "opts": ["2", "4.5", "8", "18", "24"], "ans": 2},
    {"q": "<b>2/22.</b> У коробці 48 маркерів. Синіх у 3 рази більше, ніж червоних. Скільки червоних?",
     "t": "2. Відношення, пропорції та відсотки", "type": "choice", "opts": ["12", "16", "24", "32", "36"], "ans": 0},
    {"q": "<b>3/22.</b> У ∆ABC: ∠A=40°, ∠C=80°. Знайдіть кут між висотою BH та бісектрисою BL.", "t": "31. Трикутники",
     "type": "choice", "opts": ["10°", "20°", "30°", "40°", "50°"], "ans": 1},
    {"q": "<b>4/22.</b> Обчисліть: log₂(24) - log₂(3).", "t": "20. Логарифмічні вирази", "type": "choice",
     "opts": ["3", "4", "8", "log₂(21)", "21"], "ans": 0},
    {"q": "<b>5/22.</b> Спростіть: (x² - 16) / (x² - 4x).",
     "t": "5. Розкладання на множники. Дробово-раціональні вирази", "type": "choice",
     "opts": ["(x-4)/x", "(x+4)/x", "4/x", "x+4", "x-4"], "ans": 1},
    {"q": "<b>6/22.</b> Знайдіть область визначення функції y = √(6 - 2x).", "t": "11. Функції та їх властивості",
     "type": "choice", "opts": ["[3; +∞)", "(-∞; 3]", "[-3; +∞)", "(-∞; -3]", "(-∞; +∞)"], "ans": 1},
    {"q": "<b>7/22.</b> Графік f(x) проходить через M(2; -4). Через яку точку проходить f(x - 1) + 3?",
     "t": "24. Побудова графіків функцій шляхом перетворень", "type": "choice",
     "opts": ["(1; -1)", "(3; -1)", "(1; -7)", "(3; -7)", "(2; -1)"], "ans": 1},
    {"q": "<b>8/22.</b> Знайдіть найбільший цілий розв'язок системи нерівностей:\n3x - 5 ≤ 4\n-2x &lt; 6",
     "t": "16. Системи нерівностей", "type": "choice", "opts": ["-3", "-2", "2", "3", "4"], "ans": 3},
    {
        "q": "<b>9/22.</b> Яке з тверджень правильне?\nI. Діагоналі ромба рівні.\nII. Діагоналі прямокутника перпендикулярні.\nIII. Діагоналі квадрата є бісектрисами його кутів.",
        "t": "36. Чотирикутники", "type": "choice", "opts": ["лише I", "лише II", "лише III", "I та III", "I, II, III"],
        "ans": 2},
    {"q": "<b>10/22.</b> Геометрична прогресія: b₁ = 3, q = -2. Знайдіть b₄.", "t": "25. Числові послідовності",
     "type": "choice", "opts": ["-24", "24", "-48", "-12", "16"], "ans": 0},
    {"q": "<b>11/22.</b> На тарілці 5 яблук і 7 груш. Яка ймовірність витягнути яблуко?",
     "t": "29. Початки теорії ймовірностей та елементи статистики", "type": "choice",
     "opts": ["5/7", "7/12", "5/12", "1/5", "1/12"], "ans": 2},
    {"q": "<b>12/22.</b> Вектори a(2; -1; 3) та b(m; 2; -2) перпендикулярні. Знайдіть m.",
     "t": "46. Вектори на площині та у просторі", "type": "choice", "opts": ["-4", "-2", "0", "2", "4"], "ans": 4},
    {"q": "<b>13/22.</b> Перпендикуляр AO=12 см, похила AB=13 см. Знайдіть проекцію похилої.",
     "t": "39. Вступ до стереометрії", "type": "choice", "opts": ["1 см", "5 см", "√313 см", "25 см", "√119 см"],
     "ans": 1},
    {"q": "<b>14/22.</b> Відомо: x - y = 4 та x² - y² = 20. Знайдіть x + y.", "t": "15. Системи рівнянь",
     "type": "choice", "opts": ["5", "16", "24", "80", "Неможливо"], "ans": 0},
    {"q": "<b>15/22.</b> Знайдіть значення похідної f(x) = x³ - 4x у точці x = 2.", "t": "26. Похідна",
     "type": "choice", "opts": ["0", "4", "8", "12", "24"], "ans": 2},
    {
        "q": "<b>16/22.</b> Установіть відповідність між функцією (1–3) та її властивістю (А–Д). <i>(У відповідь напишіть три літери, наприклад: <b>АБВ</b>)</i>\n\n1. y = 2/x\n2. y = 3ˣ\n3. y = cos(x)\n\nА. Графік не перетинає вісь x\nБ. Функція є непарною\nВ. Областю значень є [-1; 1]\nГ. Графік проходить через (0;0)\nД. Функція спадає на всій області",
        "t": "11. Функції та їх властивості", "type": "short", "ans": "бав"},
    {
        "q": "<b>17/22.</b> Установіть відповідність між виразом (1–3) та його значенням (А–Д), якщо a = 0.5. <i>(Напишіть три літери)</i>\n\n1. 4a + 1\n2. a⁻²\n3. |a - 1.5|\n\nА. 1\nБ. 2\nВ. 3\nГ. 4\nД. 0.5",
        "t": "3. Степені", "type": "short", "ans": "вга"},
    {
        "q": "<b>18/22.</b> Прямокутний ∆ABC (∠C=90°), катет AC = 6 см, ∠B = 30°. Відповідність між величиною (1–3) та значенням (А–Д). <i>(Напишіть три літери)</i>\n\n1. Гіпотенуза AB\n2. Катет BC\n3. Радіус описаного кола\n\nА. 6√3 см\nБ. 12 см\nВ. 3√3 см\nГ. 6 см\nД. 18 см",
        "t": "33. Прямокутний трикутник", "type": "short", "ans": "баг"},
    {
        "q": "<b>19/22.</b> Ціна смартфона становила 10 000 грн. Ціну підвищили на 20%, а потім нову ціну знизили на 15%. Якою стала ціна? <i>(Введіть число)</i>",
        "t": "2. Відношення, пропорції та відсотки", "type": "short", "ans": "10200"},
    {"q": "<b>20/22.</b> Обчисліть визначений інтеграл від 1 до 2 для функції (6x²). <i>(Введіть число)</i>",
     "t": "27. Первісна та інтеграл", "type": "short", "ans": "14"},
    {
        "q": "<b>21/22.</b> Основою прямої призми є прямокутний трикутник із катетами 6 і 8. Висота призми 10. Знайдіть об'єм. <i>(Введіть число)</i>",
        "t": "40. Призма", "type": "short", "ans": "240"},
    {"q": "<b>22/22.</b> Визначте найбільший корінь рівняння: (x² - 4x - 5)√(x - 2) = 0. <i>(Введіть число)</i>",
     "t": "10. Ірраціональні рівняння", "type": "short", "ans": "5"}
]


# ─── ФУНКЦІЇ ДЛЯ РОБОТИ З БАЗОЮ ДАНИХ ────────────────────────
@sync_to_async
def get_free_materials_urls():
    materials = StudyMaterial.objects.filter(is_published=True, is_free=True).order_by('id')
    return [mat.file.url for mat in materials if mat.file]


@sync_to_async
def get_recommendations_for_topics(wrong_topics):
    unique_topics = set(wrong_topics)
    recommendations = []
    for topic in unique_topics:
        mats = StudyMaterial.objects.filter(title__icontains=topic, is_published=True)
        if mats.exists():
            for m in mats:
                recommendations.append(m.title)
        else:
            recommendations.append(topic)
    return list(set(recommendations))


# ─── КЛАВІАТУРИ ──────────────────────────────────────────────
def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    # Інтеграція платформи прямо в Telegram
    builder.button(text="🌐 Мій кабінет (Платформа)", web_app=WebAppInfo(url="https://dokvadratu.onrender.com/cabinet/"))
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
    # Магазин тепер відкривається через WebApp
    builder.button(text="🛍️ Магазин конспектів", web_app=WebAppInfo(url="https://dokvadratu.onrender.com/materials/"))
    builder.button(text="🎁 Вся база для НМТ (1 файлом)", callback_data="download_all_free")
    builder.button(text="← До головного меню", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()


# ─── ГОЛОВНЕ МЕНЮ ТА ІНФО ────────────────────────────────────
@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    welcome_text = f"Вітаю! Це бот проєкту <b>{BOT_NAME}</b>\n\nТвій головний помічник у вивченні математики та підготовці до іспитів.\nОбери потрібний розділ нижче:"
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=get_main_menu_keyboard())


@router.callback_query(F.data == "back_main")
async def back_to_main(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
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
    text = "👨‍🏫 <b>Про мене</b>\n\nПривіт! Я — Іван, професійний викладач математики із 7-річним досвідом. У 2024–2025 роках я працював вчителем математики, а зараз продовжую роботу в державній школі..."
    builder = InlineKeyboardBuilder()
    builder.button(text="← До головного меню", callback_data="back_main")
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "menu_socials")
async def show_socials(callback: types.CallbackQuery):
    text = f"📱 <b>Мої соцмережі</b>\n\nПідписуйся, щоб отримувати розбори складних задач та лайфхаки для НМТ!\n\nЗв'язок зі мною: {CONTACT}"
    builder = InlineKeyboardBuilder()
    builder.button(text="Instagram", url="https://instagram.com/do_kvadratu")
    builder.button(text="Telegram-канал", url="https://t.me/do_kvadratu")
    builder.button(text="← До головного меню", callback_data="back_main")
    builder.adjust(1)
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "menu_nmt_main")
async def show_nmt_main(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    text = "📚 <b>Підготовка до НМТ</b>\n\nТут зібрано все необхідне для твого успіху на іспиті:"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_nmt_menu_keyboard())
    await callback.answer()


# ─── ЛОГІКА ДІАГНОСТИЧНОГО ТЕСТУ (КВІЗУ) ─────────────────────
@router.callback_query(F.data == "start_quiz")
async def start_quiz(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(score=0, current_q=0, wrong_topics=[])
    await send_quiz_question(callback.message, 0, state)
    await callback.answer()


async def send_quiz_question(message: types.Message, q_index: int, state: FSMContext):
    if q_index >= len(DIAGNOSTIC_QUESTIONS):
        await finish_quiz(message, state)
        return
    q_data = DIAGNOSTIC_QUESTIONS[q_index]
    builder = InlineKeyboardBuilder()
    if q_data["type"] == "choice":
        for i, option in enumerate(q_data["opts"]):
            builder.button(text=option, callback_data=f"qans_{i}")
        builder.adjust(2)
        builder.row(InlineKeyboardButton(text="❌ Зупинити тест", callback_data="menu_nmt_main"))
        await state.set_state(QuizFSM.answering_choice)
    else:
        builder.row(InlineKeyboardButton(text="❌ Зупинити тест", callback_data="menu_nmt_main"))
        await state.set_state(QuizFSM.answering_short)
    try:
        await message.edit_text(q_data["q"], parse_mode="HTML", reply_markup=builder.as_markup())
    except Exception:
        await message.answer(q_data["q"], parse_mode="HTML", reply_markup=builder.as_markup())


@router.callback_query(QuizFSM.answering_choice, F.data.startswith("qans_"))
async def process_quiz_choice(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    q_index = data.get("current_q", 0)
    score = data.get("score", 0)
    wrong_topics = data.get("wrong_topics", [])
    q_data = DIAGNOSTIC_QUESTIONS[q_index]
    selected_index = int(callback.data.split("_")[1])
    correct_index = q_data["ans"]
    if selected_index == correct_index:
        score += 1
    else:
        wrong_topics.append(q_data["t"])
    await state.update_data(score=score, current_q=q_index + 1, wrong_topics=wrong_topics)
    await send_quiz_question(callback.message, q_index + 1, state)
    await callback.answer()


@router.message(QuizFSM.answering_short)
async def process_quiz_short(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_index = data.get("current_q", 0)
    score = data.get("score", 0)
    wrong_topics = data.get("wrong_topics", [])
    q_data = DIAGNOSTIC_QUESTIONS[q_index]
    user_answer = message.text.lower().replace(" ", "").replace(",", "").replace(".", "").strip()
    correct_answer = str(q_data["ans"]).lower().replace(" ", "")
    if user_answer == correct_answer:
        score += 1
    else:
        wrong_topics.append(q_data["t"])
    await state.update_data(score=score, current_q=q_index + 1, wrong_topics=wrong_topics)
    try:
        await message.delete()
    except Exception:
        pass
    await send_quiz_question(message, q_index + 1, state)


async def finish_quiz(message: types.Message, state: FSMContext):
    data = await state.get_data()
    score = data.get("score", 0)
    wrong_topics = data.get("wrong_topics", [])
    total = len(DIAGNOSTIC_QUESTIONS)
    await state.clear()

    if score == total:
        level_text = "🔥 <b>Блискучий результат!</b> У тебе ідеальна база. Ти готовий(а) до найскладніших завдань."
    elif score >= total * 0.6:
        level_text = "👍 <b>Гарний рівень, але є прогалини.</b> Зверни увагу на теми, в яких були допущені помилки."
    else:
        level_text = "⚠️ <b>База потребує серйозної роботи.</b> Рекомендую терміново почати системне повторення матеріалу."

    final_text = f"🏁 <b>Діагностику завершено!</b>\n\nТвій результат: <b>{score} з {total}</b> правильних відповідей.\n{level_text}\n"
    if wrong_topics:
        recommendations = await get_recommendations_for_topics(wrong_topics)
        if recommendations:
            final_text += "\n💡 <b>Тобі варто звернути увагу на ці конспекти:</b>\n"
            for rec in recommendations:
                final_text += f"— <i>{rec}</i>\n"
            final_text += "\nУсі вони вже чекають на тебе на нашій платформі!"

    builder = InlineKeyboardBuilder()
    builder.button(text="📚 Знайти ці теми на платформі",
                   web_app=WebAppInfo(url="https://dokvadratu.onrender.com/materials/"))
    builder.button(text="← До меню НМТ", callback_data="menu_nmt_main")
    builder.adjust(1)

    try:
        await message.edit_text(final_text, parse_mode="HTML", reply_markup=builder.as_markup())
    except Exception:
        await message.answer(final_text, parse_mode="HTML", reply_markup=builder.as_markup())


# ─── БЕЗКОШТОВНІ МАТЕРІАЛИ (Вся база) ────────────────────────
@router.callback_query(F.data == "download_all_free")
async def send_all_free_materials(callback: types.CallbackQuery):
    await callback.answer()
    wait_msg = await callback.message.answer(
        "⏳ <i>Завантажую та зшиваю збірку «Вся база для НМТ». Це може зайняти близько хвилини...</i>",
        parse_mode="HTML")
    try:
        urls = await get_free_materials_urls()
        if not urls:
            await wait_msg.edit_text("На жаль, матеріалів для бази поки немає.")
            return
        writer = PdfWriter()
        async with aiohttp.ClientSession() as session:
            for file_index, url in enumerate(urls):
                if url.startswith("http://"):
                    url = url.replace("http://", "https://")
                async with session.get(url) as resp:
                    if resp.status == 200:
                        pdf_bytes = await resp.read()
                        reader = PdfReader(io.BytesIO(pdf_bytes))
                        for page_index, page in enumerate(reader.pages):
                            if file_index > 0 and page_index == 0:
                                continue
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


# ─── ПІДТРИМКА (Питання від користувачів) ────────────────────
@router.callback_query(F.data == "ask_help")
async def ask_help_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Напиши своє запитання сюди, і я відповім тобі найближчим часом:")
    await state.set_state(SupportFSM.waiting_for_question)
    await callback.answer()


@router.message(SupportFSM.waiting_for_question)
async def handle_support_question(message: types.Message, state: FSMContext):
    try:
        admin_id = int(settings.TELEGRAM_ADMIN_ID)
        await message.bot.send_message(
            admin_id,
            f"⚠️ <b>Питання від учня (Підтримка)</b>\n"
            f"Від: {message.from_user.full_name}\n"
            f"ID: <code>{message.from_user.id}</code>\n\n"
            f"<b>Текст:</b> {message.text}",
            parse_mode="HTML"
        )
    except Exception:
        pass
    builder = InlineKeyboardBuilder()
    builder.button(text="← До головного меню", callback_data="back_main")
    await message.answer("Дякую! Я отримав твоє повідомлення і скоро відпишу.", reply_markup=builder.as_markup())
    await state.clear()


# ─── АДМІНСЬКА КОМАНДА ДЛЯ НАПИСАННЯ УЧНЮ ЗА ID ───────────────
@router.message(Command("send"))
async def admin_send_message(message: types.Message):
    try:
        admin_id = int(settings.TELEGRAM_ADMIN_ID)
    except Exception:
        return

    if message.from_user.id != admin_id:
        return

    parts = message.text.split(maxsplit=2)
    if len(parts) < 3 or not parts[1].isdigit():
        await message.reply(
            "⚠️ <b>Неправильний формат!</b>\n"
            "Використовуйте: <code>/send ID_учня Текст повідомлення</code>",
            parse_mode="HTML"
        )
        return
    target_user_id = int(parts[1])
    text_to_send = parts[2]

    try:
        await message.bot.send_message(target_user_id, text_to_send, parse_mode="HTML")
        await message.reply(f"✅ Повідомлення успішно надіслано користувачу <code>{target_user_id}</code>!",
                            parse_mode="HTML")
    except Exception as e:
        await message.reply(f"❌ Не вдалося надіслати повідомлення: {e}")


# ─── АНКЕТА ЗАПИСУ НА ЗАНЯТТЯ (ЛІДОГЕНЕРАЦІЯ) ────────────────
@router.callback_query(F.data.in_(["menu_5_10", "menu_other"]))
async def start_enrollment(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    subject = "Заняття (5-10 класи)" if callback.data == "menu_5_10" else "Інші навчальні потреби"
    await state.update_data(subject=subject)
    await state.set_state(EnrollFSM.role)
    builder = InlineKeyboardBuilder()
    builder.button(text="👨‍🎓 Я учень", callback_data="role_student")
    builder.button(text="👨‍👩‍👦 Я з батьків", callback_data="role_parent")
    builder.button(text="❌ Скасувати", callback_data="back_main")
    builder.adjust(2, 1)
    text = "📝 <b>Запис на заняття</b>\n\nРадий, що ви вирішили покращити знання з математики!\nЩоб мені було зручніше спілкуватися, підкажіть, <b>хто заповнює цю анкету?</b>"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(EnrollFSM.role, F.data.startswith("role_"))
async def enroll_role(callback: types.CallbackQuery, state: FSMContext):
    role = "Учень" if callback.data == "role_student" else "Батьки"
    await state.update_data(role=role)
    await state.set_state(EnrollFSM.name)
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Скасувати", callback_data="back_main")
    if role == "Учень":
        text = "Чудово! Напиши своє <b>Ім'я та Прізвище</b>:"
    else:
        text = "Дуже приємно! Напишіть <b>Ім'я та Прізвище учня</b> (можете також вказати своє ім'я, щоб я знав, як до вас звертатися):"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())
    await callback.answer()


@router.message(EnrollFSM.name)
async def enroll_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(EnrollFSM.grade)
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Скасувати", callback_data="back_main")
    data = await state.get_data()
    text = "Супер! В якому ти зараз класі?" if data.get('role') == "Учень" else "В якому класі навчається учень?"
    await message.answer(text, reply_markup=builder.as_markup())


@router.message(EnrollFSM.grade)
async def enroll_grade(message: types.Message, state: FSMContext):
    await state.update_data(grade=message.text)
    await state.set_state(EnrollFSM.goal)
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Скасувати", callback_data="back_main")
    text = "Яка головна мета занять?\n<i>(напр., Підготовка до НМТ, підтягнути шкільну програму, розбір домашки)</i>"
    await message.answer(text, parse_mode="HTML", reply_markup=builder.as_markup())


@router.message(EnrollFSM.goal)
async def enroll_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await state.set_state(EnrollFSM.phone)
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Скасувати", callback_data="back_main")
    await message.answer(
        "Останній крок! 📱 Залиште <b>контактний номер телефону</b> (або нікнейм у Telegram) для зв'язку:",
        parse_mode="HTML", reply_markup=builder.as_markup())


@router.message(EnrollFSM.phone)
async def enroll_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone = message.text
    admin_text = (
        "🔥 <b>Нова заявка на заняття!</b>\n\n"
        f"<b>Хто залишив:</b> {data.get('role')}\n"
        f"<b>Категорія:</b> {data.get('subject')}\n"
        f"<b>Ім'я:</b> {data.get('name')}\n"
        f"<b>Клас:</b> {data.get('grade')}\n"
        f"<b>Мета:</b> {data.get('goal')}\n"
        f"<b>Контакт:</b> {phone}\n\n"
        f"<b>Telegram ID:</b> <code>{message.from_user.id}</code>\n"
    )
    try:
        admin_id = int(settings.TELEGRAM_ADMIN_ID)
        await message.bot.send_message(admin_id, admin_text, parse_mode="HTML")
    except Exception:
        pass
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.button(text="← До головного меню", callback_data="back_main")
    await message.answer(
        "✅ <b>Заявку успішно відправлено!</b>\n\nЯ зв'яжуся з вами найближчим часом, щоб обговорити деталі та підібрати зручний розклад.",
        parse_mode="HTML", reply_markup=builder.as_markup())


# ─── ПЕРЕХОПЛЮВАЧ УСІХ ПОВІДОМЛЕНЬ ──────────────────────────
@router.message(F.text & ~F.text.startswith('/'))
async def catch_all_text(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        try:
            admin_id = int(settings.TELEGRAM_ADMIN_ID)
            await message.bot.send_message(
                admin_id,
                f"💬 <b>Повідомлення від учня</b>\n"
                f"Від: {message.from_user.full_name}\n"
                f"ID: <code>{message.from_user.id}</code>\n\n"
                f"<b>Текст:</b> {message.text}\n\n"
                f"<i>Щоб відповісти, просто напишіть йому в особисті повідомлення за ID.</i>",
                parse_mode="HTML"
            )
        except Exception:
            pass
        builder = InlineKeyboardBuilder()
        builder.button(text="← До головного меню", callback_data="back_main")
        await message.answer(
            "Передав твоє повідомлення! Відповім тобі найближчим часом 😉",
            reply_markup=builder.as_markup()
        )