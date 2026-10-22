"""Нагадування в Telegram (бот @do_kvadratu_bot): учень підключає бота в кабінеті, і раз на день сайт надсилає
нагадування про ДЗ на завтра, кінець підписки на клас, покинуту практику й заняття завтра (викладачеві — його
розклад на завтра). За LESSON_SOON до заняття — ще одне нагадування. Кожне — лише раз (ReminderLog).

Запуск: сам сайт раз на день у SEND_HOURS за Києвом — перший запит у цей час запускає розсилку у фоні
(maybe_send_daily, викликає middleware); нагадування «скоро заняття» — щонайчастіше раз на SOON_EVERY хвилин
(maybe_send_soon); вручну — `python manage.py send_reminders`."""
import datetime
import logging
import threading

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import IntegrityError, close_old_connections, transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import constant_time_compare, salted_hmac

from .models import ClassSubscription, Homework, Lesson, PracticeRun, ReminderLog

logger = logging.getLogger(__name__)

BOT_USERNAME = 'do_kvadratu_bot'
SEND_HOURS = range(16, 21)          # після уроків, але не пізно ввечері
SUBSCRIPTION_DAYS_BEFORE = 3
PRACTICE_IDLE = (datetime.timedelta(days=1), datetime.timedelta(days=7))   # кинута день-тиждень тому
LESSON_SOON = datetime.timedelta(hours=2)
SOON_EVERY = 10                     # хвилин між перевірками «скоро заняття»


# ─── ПРИВ'ЯЗКА TELEGRAM ДО АКАУНТА ───────────────────────────
def link_payload(user):
    """Параметр для t.me/<бот>?start=… : id користувача й підпис (Telegram дозволяє лише A-Z, a-z, 0-9, _ і -)."""
    return f'link{user.id}_{salted_hmac("telegram-link", str(user.id)).hexdigest()[:20]}'


def link_url(user):
    return f'https://t.me/{BOT_USERNAME}?start={link_payload(user)}'


def user_from_payload(payload):
    """Користувач за параметром із link_payload, або None (чужий чи підроблений параметр)."""
    if not payload.startswith('link') or '_' not in payload:
        return None
    user_id, _ = payload[4:].split('_', 1)
    user = get_user_model().objects.filter(id=int(user_id)).first() if user_id.isdigit() else None
    return user if user and constant_time_compare(link_payload(user), payload) else None


def link_chat(user, chat_id):
    """Один чат — один акаунт: прив'язка до нового акаунта знімає її зі старого."""
    get_user_model().objects.filter(telegram_id=str(chat_id)).exclude(pk=user.pk).update(telegram_id=None)
    user.telegram_id = str(chat_id)
    user.save(update_fields=['telegram_id'])


def unlink_chat(chat_id):
    return get_user_model().objects.filter(telegram_id=str(chat_id)).update(telegram_id=None)


# ─── ЩО НАГАДАТИ ─────────────────────────────────────────────
def site_url(path):
    return settings.SITE_URL + path


def due_reminders(today=None, now=None):
    """[(user, ключ, текст, (підпис кнопки, адреса))] — усе, що варто нагадати зараз (без перевірки, чи вже
    надсилали)."""
    today = today or timezone.localdate()
    now = now or timezone.now()
    reminders = []

    for hw in (Homework.objects.filter(attempt__isnull=True, due_date__gte=today,
                                       due_date__lte=today + datetime.timedelta(days=1),
                                       student__status='approved', student__user__telegram_id__isnull=False)
               .exclude(student__user__telegram_id='').select_related('student__user', 'material')
               .defer('material__html_content')):
        when = 'сьогодні' if hw.due_date == today else 'завтра'
        reminders.append((hw.student.user, f'hw:{hw.id}',
                          f"📝 Домашнє завдання «{hw.material.title}» треба виконати {when} "
                          f"({hw.due_date:%d.%m}).",
                          ('Виконати ДЗ', site_url(reverse('practice_session', args=[hw.material_id])))))

    soon = today + datetime.timedelta(days=SUBSCRIPTION_DAYS_BEFORE)
    for sub in (ClassSubscription.objects.filter(valid_until__gte=today, valid_until__lte=soon,
                                                 user__telegram_id__isnull=False)
                .exclude(user__telegram_id='').select_related('user')):
        # Уже продовжено (є підписка на той самий клас, що діє довше) — не нагадуємо
        if ClassSubscription.objects.filter(user=sub.user, number=sub.number,
                                            valid_until__gt=sub.valid_until).exists():
            continue
        what = 'Підписка з супроводом' if sub.with_support else 'Підписка'
        reminders.append((sub.user, f'sub:{sub.id}',
                          f"🎒 {what} на {sub.number} клас закінчується {sub.valid_until:%d.%m}. "
                          f"Продовжте, щоб не втратити доступ до уроків і практики.",
                          ('Продовжити',
                           site_url(reverse('class_subscribe') + f'?class={sub.number}#class-{sub.number}'))))

    idle_from, idle_to = now - PRACTICE_IDLE[1], now - PRACTICE_IDLE[0]
    seen_users = set()
    for run in (PracticeRun.objects.filter(finished_at__isnull=True, teacher__isnull=True,
                                           updated_at__gte=idle_from, updated_at__lte=idle_to,
                                           user__telegram_id__isnull=False)
                .exclude(user__telegram_id='').select_related('user', 'material')
                .defer('material__html_content').order_by('-updated_at')):
        if run.user_id in seen_users:   # одна практика на учня за раз — найсвіжіша
            continue
        seen_users.add(run.user_id)
        reminders.append((run.user, f'run:{run.id}',
                          f"💪 Ви почали практику «{run.material.title}» і зупинилися на півдорозі. "
                          f"Продовжте з того самого місця — це кілька хвилин.",
                          ('Продовжити практику', site_url(reverse('practice_session', args=[run.material_id])))))

    reminders += lessons_tomorrow(today)
    return reminders


def lesson_key(prefix, lesson):
    # Час у ключі: перенесене заняття нагадаємо ще раз, уже з новим часом
    return f'{prefix}:{lesson.id}:{timezone.localtime(lesson.start):%y%m%d%H%M}'


def planned_lessons(start_from, start_to):
    from .schedule import fill_series
    fill_series(until=timezone.localtime(start_to).date())
    return (Lesson.objects.filter(status='planned', start__gte=start_from, start__lt=start_to,
                                  student__status='approved')
            .select_related('student__user', 'teacher').order_by('start'))


def lessons_tomorrow(today):
    """Учневі — про кожне заняття завтра; викладачеві — один лист із розкладом на завтра."""
    from .schedule import aware, teacher_name
    tomorrow = today + datetime.timedelta(days=1)
    lessons = list(planned_lessons(aware(tomorrow, datetime.time.min),
                                   aware(tomorrow + datetime.timedelta(days=1), datetime.time.min)))
    reminders, by_teacher = [], {}
    for lesson in lessons:
        pupil = lesson.student.user
        if pupil.telegram_id:
            reminders.append((pupil, lesson_key('lesson', lesson),
                              f"📅 Завтра о {timezone.localtime(lesson.start):%H:%M} — заняття з математики "
                              f"({teacher_name(lesson.teacher)}).",
                              ('Мій розклад', site_url(reverse('cabinet') + '#learn'))))
        by_teacher.setdefault(lesson.teacher, []).append(lesson)
    for teacher, items in by_teacher.items():
        if not teacher.telegram_id:
            continue
        rows = '\n'.join(f"• {timezone.localtime(lesson.start):%H:%M} — {lesson.student.real_name}"
                         for lesson in items)
        reminders.append((teacher, f'day:{teacher.id}:{tomorrow:%y%m%d}',
                          f"🗓 Завтра ({tomorrow:%d.%m}) у вас заняття:\n{rows}",
                          ('Розклад', site_url(reverse('schedule') + f'?week={tomorrow:%Y-%m-%d}'))))
    return reminders


def lessons_soon(now=None):
    """Учневі — за LESSON_SOON до кожного заняття."""
    now = now or timezone.now()
    reminders = []
    for lesson in planned_lessons(now, now + LESSON_SOON):
        pupil = lesson.student.user
        if pupil.telegram_id:
            reminders.append((pupil, lesson_key('soon', lesson),
                              f"⏰ Сьогодні о {timezone.localtime(lesson.start):%H:%M} заняття з математики. "
                              f"Підготуйте зошит і домашнє завдання!",
                              ('Мій розклад', site_url(reverse('cabinet') + '#learn'))))
    return reminders


# ─── НАДСИЛАННЯ ──────────────────────────────────────────────
def send_message(chat_id, text, button=None):
    """True — надіслано; False — не вдалося; None — бот заблоковано (чат більше недоступний)."""
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    if not token:
        return False
    payload = {'chat_id': chat_id, 'text': text}
    if button:
        payload['reply_markup'] = {'inline_keyboard': [[{'text': button[0], 'url': button[1]}]]}
    try:
        response = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json=payload, timeout=5)
    except requests.RequestException:
        logger.warning("Нагадування в Telegram не надіслано: немає зв'язку")
        return False
    if response.status_code == 403:
        return None
    if not response.ok:
        logger.warning("Telegram відхилив нагадування: %s %s", response.status_code, response.text[:300])
    return response.ok


def send_due_reminders(items=None):
    """Надсилає ще не надіслані нагадування (за замовчуванням — щоденні); повертає кількість надісланих."""
    sent = 0
    for user, key, text, button in (due_reminders() if items is None else items):
        try:
            with transaction.atomic():
                log = ReminderLog.objects.create(user=user, key=key)   # унікальний ключ — двічі не надішлемо
        except IntegrityError:
            continue
        result = send_message(user.telegram_id, text, button)
        if result:
            sent += 1
        elif result is None:   # учень заблокував бота — більше не пишемо
            unlink_chat(user.telegram_id)
        else:
            log.delete()       # спробуємо наступного разу
    return sent


def maybe_send_daily():
    """Раз на день у SEND_HOURS запускає розсилку у фоні (без бота — нічого не робить)."""
    if not (getattr(settings, 'REMINDERS_DAILY', True) and getattr(settings, 'TELEGRAM_BOT_TOKEN', '')):
        return
    now = timezone.localtime()
    if now.hour not in SEND_HOURS or not cache.add(f'reminders-{now.date()}', True, 60 * 60 * 25):
        return

    def run():
        try:
            sent = send_due_reminders()
            if sent:
                logger.info("Нагадувань у Telegram надіслано: %s", sent)
        except Exception:
            logger.exception("Помилка розсилки нагадувань")
        finally:
            close_old_connections()

    threading.Thread(target=run, daemon=True).start()


def maybe_send_soon():
    """Раз на SOON_EVERY хвилин (з 7 до 22) — нагадування про заняття, що почнуться за LESSON_SOON."""
    if not (getattr(settings, 'REMINDERS_DAILY', True) and getattr(settings, 'TELEGRAM_BOT_TOKEN', '')):
        return
    now = timezone.localtime()
    slot = now.hour * 60 + now.minute
    if not 7 <= now.hour < 22 or not cache.add(f'reminders-soon-{now.date()}-{slot // SOON_EVERY}', True, 60 * 60):
        return

    def run():
        try:
            send_due_reminders(lessons_soon())
        except Exception:
            logger.exception("Помилка нагадувань про заняття")
        finally:
            close_old_connections()

    threading.Thread(target=run, daemon=True).start()


class DailyRemindersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        maybe_send_daily()
        maybe_send_soon()
        return response
