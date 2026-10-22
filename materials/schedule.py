"""Розклад занять викладача: тиждень у кабінеті, разові й постійні заняття, перенесення, скасування, звіт після
заняття. Учень і батьки бачать найближчі заняття, бот нагадує про них (reminders.py), розклад можна підписати
в Google/Apple-календарі (calendar_feed — iCalendar за підписаним посиланням).

Постійне заняття — LessonSeries; його дати створюються рядками Lesson на FILL_WEEKS наперед (fill_series), тож
кожну дату можна перенести чи скасувати окремо. «Усі наступні» розриває серію: стара закінчується, нова
починається з нової дати."""
import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import urlencode
from django.views.decorators.http import require_POST

from . import homework, teachers
from .forms import StudentReportForm
from .models import (NMT_SUBJECT_NAME, CurriculumTopic, Lesson, LessonSeries, PracticeAttempt, StudentReport,
                     TutorStudentRequest)

FILL_WEEKS = 10                      # на скільки тижнів наперед створювати дати постійних занять
FILL_BACK = datetime.timedelta(days=14)
DURATIONS = (30, 45, 50, 60, 90, 120)
REPORT_DAYS = 30                     # заняття без звіту за останні REPORT_DAYS днів — у «Чекають звіту»
NOTIFY_DAYS = 14                     # про зміни в розкладі далі ніж на NOTIFY_DAYS наперед учневі не пишемо
WEEKDAYS_SHORT = ('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'нд')
WEEKDAYS_EVERY = ('щопонеділка', 'щовівторка', 'щосереди', 'щочетверга', "щоп'ятниці", 'щосуботи', 'щонеділі')
MONTHS = ('січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 'липня', 'серпня', 'вересня', 'жовтня',
          'листопада', 'грудня')


# ─── ДАТИ ПОСТІЙНИХ ЗАНЯТЬ ───────────────────────────────────
def aware(day, time):
    return timezone.make_aware(datetime.datetime.combine(day, time))


def fill_series(series_qs=None, until=None):
    """Створює ще не створені дати постійних занять до until (за замовчуванням — FILL_WEEKS наперед).
    Перенесене чи скасоване заняття серія не відтворює: дата серії (series_date) у нього лишається."""
    today = timezone.localdate()
    until = until or today + datetime.timedelta(weeks=FILL_WEEKS)
    series_qs = LessonSeries.objects.all() if series_qs is None else series_qs
    for series in series_qs.filter(Q(ends_on__isnull=True) | Q(ends_on__gte=today - FILL_BACK),
                                   starts_on__lte=until):
        last = min(until, series.ends_on or until)
        day = max(series.starts_on, today - FILL_BACK)
        day += datetime.timedelta(days=(series.weekday - day.weekday()) % 7)
        existing = set(series.lessons.values_list('series_date', flat=True))
        new = []
        while day <= last:
            if day not in existing:
                new.append(Lesson(teacher_id=series.teacher_id, student_id=series.student_id, series=series,
                                  series_date=day, start=aware(day, series.time), duration=series.duration,
                                  note=series.note))
            day += datetime.timedelta(weeks=1)
        if new:
            Lesson.objects.bulk_create(new, ignore_conflicts=True)


def end_series(series, from_day):
    """Серія закінчується перед from_day: її заплановані дати від from_day (не перенесені окремо, без звіту)
    зникають."""
    series.ends_on = from_day - datetime.timedelta(days=1)
    series.save(update_fields=['ends_on'])
    series.lessons.filter(series_date__gte=from_day, status__in=('planned', 'cancelled'), moved_from__isnull=True,
                          report__isnull=True).delete()


def lesson_series_day(lesson):
    return lesson.series_date or timezone.localtime(lesson.start).date()


# ─── ПІДПИСИ ─────────────────────────────────────────────────
def when_label(start, today=None):
    """«сьогодні о 15:00», «завтра о 15:00», «пт, 24 жовтня о 15:00»."""
    today = today or timezone.localdate()
    local = timezone.localtime(start)
    day = local.date()
    if day == today:
        prefix = 'сьогодні'
    elif day == today + datetime.timedelta(days=1):
        prefix = 'завтра'
    else:
        prefix = f'{WEEKDAYS_SHORT[day.weekday()]}, {day.day} {MONTHS[day.month - 1]}'
    return f'{prefix} о {local:%H:%M}'


def teacher_name(user):
    return user.get_full_name() or user.email or user.username


def annotate(lessons):
    """Підписи для шаблонів: час, кінець, тиждень, чи вже минуло."""
    now = timezone.now()
    for lesson in lessons:
        local = timezone.localtime(lesson.start)
        lesson.local_start = local
        lesson.local_end = timezone.localtime(lesson.end)
        lesson.when = when_label(lesson.start)
        lesson.is_past = lesson.end <= now
        lesson.needs_report = lesson.is_past and lesson.status == 'planned'
    return lessons


# ─── ХТО ЩО БАЧИТЬ ───────────────────────────────────────────
def upcoming_for_student(student, limit=5):
    """Найближчі заплановані заняття учня (TutorStudentRequest), зокрема те, що йде зараз."""
    fill_series(LessonSeries.objects.filter(student=student))
    lessons = (Lesson.objects.filter(student=student, status='planned',
                                     start__gte=timezone.now() - datetime.timedelta(hours=4))
               .select_related('teacher', 'curriculum_topic').order_by('start'))
    return annotate([lesson for lesson in lessons[:limit + 4] if lesson.end > timezone.now()][:limit])


def awaiting_report(teacher):
    """Минулі заняття без звіту за останні REPORT_DAYS днів."""
    now = timezone.now()
    lessons = (Lesson.objects.filter(teacher=teacher, status='planned', start__lt=now,
                                     start__gte=now - datetime.timedelta(days=REPORT_DAYS))
               .select_related('student', 'curriculum_topic').order_by('-start'))
    return [lesson for lesson in annotate(list(lessons)) if lesson.is_past]


def teacher_overview(teacher):
    """Для кабінету викладача: заняття сьогодні й завтра і ті, що чекають звіту."""
    fill_series(LessonSeries.objects.filter(teacher=teacher))
    today = timezone.localdate()
    lessons = annotate(list(
        Lesson.objects.filter(teacher=teacher, start__gte=aware(today, datetime.time.min),
                              start__lt=aware(today + datetime.timedelta(days=2), datetime.time.min))
        .select_related('student', 'curriculum_topic').order_by('start')))
    days = [(f'Сьогодні, {today:%d.%m}', [lesson for lesson in lessons if lesson.local_start.date() == today]),
            ('Завтра', [lesson for lesson in lessons if lesson.local_start.date() != today])]
    return {'days': days, 'awaiting_report': awaiting_report(teacher)[:10]}


# ─── ЗВІТ ЗАНЯТТЯ ────────────────────────────────────────────
# Звіт пишуть і зі сторінки результатів практики на уроці чи з кабінету (views.add_quick_report), і з розкладу.
# Щоб звіт за день не дублювався, він прив'язується до заняття того дня (Lesson.report).
def attach_report(lesson, report):
    lesson.report = report
    lesson.status = 'done'
    lesson.curriculum_topic = report.curriculum_topic or lesson.curriculum_topic
    lesson.save(update_fields=['report', 'status', 'curriculum_topic'])


def lesson_for_report(teacher, student, day):
    """Заняття, до якого належить звіт за день day: того дня, ще без звіту, не скасоване; якщо таких кілька —
    найближче до цієї миті."""
    lessons = Lesson.objects.filter(teacher=teacher, student=student, report__isnull=True,
                                    start__gte=aware(day, datetime.time.min),
                                    start__lt=aware(day + datetime.timedelta(days=1), datetime.time.min)
                                    ).exclude(status='cancelled')
    now = timezone.now()
    return min(lessons, key=lambda lesson: abs(lesson.start - now), default=None)


def link_report(teacher, report):
    """Новий звіт (з практики чи кабінету) закриває заняття того дня в розкладі; повертає заняття або None."""
    day = report.date
    if isinstance(day, datetime.datetime):   # типова дата звіту — timezone.now, у пам'яті це ще момент в UTC
        day = timezone.localtime(day).date()
    lesson = lesson_for_report(teacher, report.student, day)
    if lesson:
        attach_report(lesson, report)
    return lesson


def mark_held(teacher, student):
    """Результат з уроку без звіту (бал НМТ) — сьогоднішнє заняття учня відбулося."""
    lesson = lesson_for_report(teacher, student, timezone.localdate())
    if lesson and lesson.status == 'planned':
        lesson.status = 'done'
        lesson.save(update_fields=['status'])


def lesson_practice(lesson):
    """Остання практика учня, яку вчитель провів на цьому занятті (того ж дня), — з неї беремо оцінки й тему."""
    day = timezone.localtime(lesson.start).date()
    return (PracticeAttempt.objects.filter(user_id=lesson.student.user_id, conducted_by=lesson.teacher,
                                           nush_modeling__isnull=False,
                                           created_at__gte=aware(day, datetime.time.min),
                                           created_at__lt=aware(day + datetime.timedelta(days=1), datetime.time.min))
            .select_related('material').defer('material__html_content').order_by('-created_at').first())


def own_lesson(request, lesson_id):
    if not teachers.is_tutor(request.user):
        raise Http404
    return get_object_or_404(Lesson.objects.select_related('student__user', 'series'), id=lesson_id,
                             teacher=request.user)


def report_topics(teacher):
    """Теми для звіту — як у кабінеті: шкільні теми класів підписки викладача."""
    topics = CurriculumTopic.objects.exclude(chapter__grade__subject__name=NMT_SUBJECT_NAME)
    grades = teachers.licensed_grade_ids(teacher)
    if grades is not None:
        topics = topics.filter(chapter__grade_id__in=grades)
    return topics.select_related('chapter__grade').order_by(
        'chapter__grade__subject__order', 'chapter__grade__order', 'chapter__order', 'order')


# ─── ПІДПИСКА В КАЛЕНДАРІ (iCalendar) ────────────────────────
def feed_token(kind, user_id):
    """t — розклад викладача, s — заняття учня. Підпис не дає підібрати чужий розклад."""
    return f'{kind}{user_id}-{salted_hmac("lesson-calendar", f"{kind}{user_id}").hexdigest()[:24]}'


def feed_links(path):
    """Посилання для підписки: https (скопіювати), webcal:// (Apple, Outlook) і Google Календар."""
    url = settings.SITE_URL + path
    webcal = 'webcal://' + url.split('://', 1)[1]
    return {'url': url, 'webcal': webcal,
            'google': 'https://calendar.google.com/calendar/render?' + urlencode({'cid': webcal})}


def feed_lessons_for_token(token):
    head = token.partition('-')[0]
    kind, user_id = head[:1], head[1:]
    if not user_id.isdigit() or not constant_time_compare(feed_token(kind, int(user_id)), token):
        raise Http404
    user_id = int(user_id)
    if kind == 't':
        fill_series(LessonSeries.objects.filter(teacher_id=user_id))
        return Lesson.objects.filter(teacher_id=user_id), 'Розклад занять — ДО КВАДРАТУ', True
    if kind == 's':
        fill_series(LessonSeries.objects.filter(student__user_id=user_id))
        return Lesson.objects.filter(student__user_id=user_id), 'Заняття з математики — ДО КВАДРАТУ', False
    raise Http404


def ics_escape(text):
    return (text.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace('\r', '')
            .replace('\n', '\\n'))


def ics_fold(line):
    """Рядки iCalendar — не довші за 75 байтів; продовження починається з пробілу (UTF-8 не розриваємо)."""
    out, current = [], ''
    for char in line:
        limit = 75 if not out else 74
        if len((current + char).encode()) > limit:
            out.append(current)
            current = char
        else:
            current += char
    out.append(current)
    return '\r\n '.join(out)


def ics_time(moment):
    return moment.astimezone(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def build_ics(lessons, title, for_teacher):
    host = settings.SITE_URL.split('://', 1)[-1]
    lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//dokvadratu.com.ua//Rozklad//UK', 'CALSCALE:GREGORIAN',
             'METHOD:PUBLISH', f'X-WR-CALNAME:{ics_escape(title)}', 'X-WR-TIMEZONE:Europe/Kyiv',
             'REFRESH-INTERVAL;VALUE=DURATION:PT1H', 'X-PUBLISHED-TTL:PT1H']
    stamp = ics_time(timezone.now())
    for lesson in lessons:
        summary = (f'Заняття: {lesson.student.real_name}' if for_teacher
                   else f'Математика з {teacher_name(lesson.teacher)}')
        details = [lesson.curriculum_topic.name if lesson.curriculum_topic else '', lesson.note]
        lines += ['BEGIN:VEVENT', f'UID:lesson-{lesson.id}@{host}', f'DTSTAMP:{stamp}',
                  f'DTSTART:{ics_time(lesson.start)}', f'DTEND:{ics_time(lesson.end)}',
                  f'SUMMARY:{ics_escape(summary)}',
                  'STATUS:' + ('CANCELLED' if lesson.status == 'cancelled' else 'CONFIRMED')]
        description = '\n'.join(part for part in details if part)
        if description:
            lines.append(f'DESCRIPTION:{ics_escape(description)}')
        lines.append('END:VEVENT')
    lines.append('END:VCALENDAR')
    return '\r\n'.join(ics_fold(line) for line in lines) + '\r\n'


def ics_response(lessons, title, for_teacher):
    since = timezone.now() - datetime.timedelta(days=60)
    lessons = lessons.filter(start__gte=since).select_related('student', 'teacher', 'curriculum_topic')
    response = HttpResponse(build_ics(lessons, title, for_teacher), content_type='text/calendar; charset=utf-8')
    response['Content-Disposition'] = 'inline; filename="rozklad.ics"'
    response['Cache-Control'] = 'private, max-age=900'
    response['X-Robots-Tag'] = 'noindex'
    return response


def calendar_feed(request, token):
    lessons, title, for_teacher = feed_lessons_for_token(token)
    return ics_response(lessons, title, for_teacher)


def parent_calendar_feed(request, parent_token):
    student = get_object_or_404(TutorStudentRequest, parent_token=parent_token, status='approved')
    fill_series(LessonSeries.objects.filter(student=student))
    return ics_response(Lesson.objects.filter(student=student), f'Заняття: {student.real_name} — ДО КВАДРАТУ', False)


def student_feed_links(user):
    return feed_links(reverse('calendar_feed', args=[feed_token('s', user.id)]))


def teacher_feed_links(user):
    return feed_links(reverse('calendar_feed', args=[feed_token('t', user.id)]))


# ─── ПОВІДОМЛЕННЯ УЧНЕВІ ─────────────────────────────────────
def notify_student(student, text):
    """Зміна в розкладі — одразу учневі в Telegram (якщо бот підключено)."""
    from . import reminders
    chat = student.user.telegram_id
    if not chat:
        return
    result = reminders.send_message(chat, text, ('Мій розклад', reminders.site_url(reverse('cabinet') + '#learn')))
    if result is None:
        reminders.unlink_chat(chat)


def soon(start):
    return start <= timezone.now() + datetime.timedelta(days=NOTIFY_DAYS)


# ─── ФОРМИ ───────────────────────────────────────────────────
def parse_when(post):
    """(початок, тривалість) з полів date, time, duration або (None, None, помилка)."""
    try:
        day = datetime.date.fromisoformat(post.get('date', ''))
        time = datetime.time.fromisoformat(post.get('time', ''))
    except ValueError:
        return None, None, 'Вкажіть дату й час заняття.'
    duration = post.get('duration', '60')
    duration = int(duration) if duration.isdigit() else 0
    if not 15 <= duration <= 240:
        return None, None, 'Тривалість — від 15 до 240 хвилин.'
    return aware(day, time.replace(second=0, microsecond=0, tzinfo=None)), duration, None


def overlaps(teacher, start, duration, exclude_id=None):
    """Заплановані заняття викладача, що перетинаються з новим часом (попередження, не заборона)."""
    end = start + datetime.timedelta(minutes=duration)
    nearby = (Lesson.objects.filter(teacher=teacher, status='planned', start__lt=end,
                                    start__gte=start - datetime.timedelta(hours=4))
              .exclude(id=exclude_id).select_related('student'))
    return [lesson for lesson in nearby if lesson.end > start]


def warn_overlaps(request, start, duration, exclude_id=None):
    clash = overlaps(request.user, start, duration, exclude_id)
    if clash:
        names = ', '.join(f'{lesson.student.real_name} ({timezone.localtime(lesson.start):%H:%M})' for lesson in clash)
        messages.warning(request, f'⚠ У цей час уже є заняття: {names}.')


def week_url(day):
    monday = day - datetime.timedelta(days=day.weekday())
    return reverse('schedule') + f'?week={monday:%Y-%m-%d}'


def back_to_week(request, day=None):
    week = request.POST.get('week', '')
    try:
        day = datetime.date.fromisoformat(week) if week else day
    except ValueError:
        pass
    return redirect(week_url(day or timezone.localdate()))


# ─── СТОРІНКИ ────────────────────────────────────────────────
@login_required
def schedule_week(request):
    if not teachers.is_tutor(request.user):
        return redirect('cabinet')
    today = timezone.localdate()
    try:
        day = datetime.date.fromisoformat(request.GET.get('week', ''))
    except ValueError:
        day = today
    monday = day - datetime.timedelta(days=day.weekday())
    sunday = monday + datetime.timedelta(days=6)
    fill_series(LessonSeries.objects.filter(teacher=request.user),
                until=max(sunday, today + datetime.timedelta(weeks=FILL_WEEKS)))
    lessons = annotate(list(
        Lesson.objects.filter(teacher=request.user, start__gte=aware(monday, datetime.time.min),
                              start__lt=aware(sunday + datetime.timedelta(days=1), datetime.time.min))
        .select_related('student', 'curriculum_topic', 'series').order_by('start')))
    days = []
    for offset in range(7):
        date = monday + datetime.timedelta(days=offset)
        days.append({'date': date, 'name': WEEKDAYS_SHORT[offset], 'is_today': date == today,
                     'month': MONTHS[date.month - 1],
                     'lessons': [lesson for lesson in lessons if lesson.local_start.date() == date]})
    students = teachers.students_of(request.user).order_by('real_name')
    series = (LessonSeries.objects.filter(teacher=request.user)
              .filter(Q(ends_on__isnull=True) | Q(ends_on__gte=today)).select_related('student'))
    planned = [lesson for lesson in lessons if lesson.status != 'cancelled']
    context = {
        'days': days, 'monday': monday, 'sunday': sunday, 'today': today,
        'month_from': MONTHS[monday.month - 1], 'month_to': MONTHS[sunday.month - 1],
        'prev_week': week_url(monday - datetime.timedelta(weeks=1)),
        'next_week': week_url(monday + datetime.timedelta(weeks=1)),
        'this_week': week_url(today), 'is_this_week': monday <= today <= sunday,
        'students': students, 'series': series, 'durations': DURATIONS,
        'weekdays_every': WEEKDAYS_EVERY,
        'week_hours': round(sum(lesson.duration for lesson in planned) / 60, 1), 'week_count': len(planned),
        'awaiting_report': awaiting_report(request.user),
        'default_date': today if monday <= today <= sunday else monday,
        'feed': teacher_feed_links(request.user),
    }
    for item in series:
        item.every = WEEKDAYS_EVERY[item.weekday]
    return render(request, 'materials/schedule.html', context)


@login_required
@require_POST
def schedule_add(request):
    if not teachers.is_tutor(request.user):
        return redirect('cabinet')
    student_id = request.POST.get('student_id', '')
    student = get_object_or_404(teachers.students_of(request.user), id=int(student_id) if student_id.isdigit() else 0)
    start, duration, error = parse_when(request.POST)
    if error:
        messages.error(request, error)
        return back_to_week(request)
    local = timezone.localtime(start)
    note = request.POST.get('note', '').strip()[:200]
    warn_overlaps(request, start, duration)
    if request.POST.get('repeat') == 'weekly':
        series = LessonSeries.objects.create(teacher=request.user, student=student, weekday=local.weekday(),
                                             time=local.time(), duration=duration, starts_on=local.date(), note=note)
        fill_series(LessonSeries.objects.filter(id=series.id))
        every = f'{WEEKDAYS_EVERY[local.weekday()]} о {local:%H:%M}'
        messages.success(request, f'✅ Постійне заняття: {student.real_name}, {every}, з {local:%d.%m}.')
        notify_student(student, f'📅 У вашому розкладі нове постійне заняття: {every}, '
                                f'починаючи з {local:%d.%m}.')
    else:
        Lesson.objects.create(teacher=request.user, student=student, start=start, duration=duration, note=note)
        messages.success(request, f'✅ Заняття додано: {student.real_name}, {when_label(start)}.')
        if soon(start):
            notify_student(student, f'📅 Нове заняття: {when_label(start)}.')
    return redirect(week_url(local.date()))


@login_required
@require_POST
def schedule_move(request, lesson_id):
    lesson = own_lesson(request, lesson_id)
    start, duration, error = parse_when(request.POST)
    if error:
        messages.error(request, error)
        return back_to_week(request)
    if lesson.report_id:
        messages.error(request, 'Заняття вже має звіт — його не переносять.')
        return back_to_week(request)
    old = lesson.start
    local = timezone.localtime(start)
    warn_overlaps(request, start, duration, exclude_id=lesson.id)
    if request.POST.get('scope') == 'following' and lesson.series:
        old_series = lesson.series
        with transaction.atomic():
            end_series(old_series, lesson_series_day(lesson))
            new_series = LessonSeries.objects.create(
                teacher=request.user, student=lesson.student, weekday=local.weekday(), time=local.time(),
                duration=duration, starts_on=local.date(), note=old_series.note)
            if Lesson.objects.filter(id=lesson.id).exists():   # окремо перенесене заняття end_series лишає
                lesson.delete()
            fill_series(LessonSeries.objects.filter(id=new_series.id))
        every = f'{WEEKDAYS_EVERY[local.weekday()]} о {local:%H:%M}'
        messages.success(request, f'✅ Постійне заняття перенесено: {lesson.student.real_name}, {every}, '
                                  f'з {local:%d.%m}.')
        notify_student(lesson.student, f'🔁 Постійне заняття перенесено: тепер {every}, починаючи з {local:%d.%m}.')
        return redirect(week_url(local.date()))

    lesson.start, lesson.duration = start, duration
    lesson.moved_from = lesson.moved_from or old
    if lesson.moved_from == start:   # повернули на початковий час
        lesson.moved_from = None
    lesson.status = 'planned'
    lesson.save()
    messages.success(request, f'✅ Заняття перенесено на {when_label(start)}.')
    if soon(start) or soon(old):
        notify_student(lesson.student, f'🔁 Заняття {when_label(old)} перенесено на {when_label(start)}.')
    return redirect(week_url(local.date()))


@login_required
@require_POST
def schedule_cancel(request, lesson_id):
    lesson = own_lesson(request, lesson_id)
    if lesson.report_id:
        messages.error(request, 'Заняття вже має звіт — його не скасовують.')
        return back_to_week(request)
    if request.POST.get('scope') == 'following' and lesson.series:
        series = lesson.series
        with transaction.atomic():
            end_series(series, lesson_series_day(lesson))
            Lesson.objects.filter(id=lesson.id, status='planned', report__isnull=True).delete()
        messages.success(request, f'Постійне заняття {lesson.student.real_name} завершено '
                                  f'(останнє — {series.ends_on:%d.%m}).')
        notify_student(lesson.student, f'❌ Постійне заняття ({WEEKDAYS_EVERY[series.weekday]} о '
                                       f'{series.time:%H:%M}) більше не відбуватиметься, починаючи з '
                                       f'{when_label(lesson.start).split(" о ")[0]}.')
        return back_to_week(request, timezone.localtime(lesson.start).date())
    lesson.status = 'cancelled'
    lesson.save(update_fields=['status'])
    messages.success(request, f'Заняття {when_label(lesson.start)} скасовано.')
    if soon(lesson.start) and lesson.start > timezone.now():
        notify_student(lesson.student, f'❌ Заняття {when_label(lesson.start)} скасовано.')
    return back_to_week(request, timezone.localtime(lesson.start).date())


@login_required
@require_POST
def schedule_restore(request, lesson_id):
    lesson = own_lesson(request, lesson_id)
    if lesson.status == 'cancelled':
        lesson.status = 'planned'
        lesson.save(update_fields=['status'])
        messages.success(request, f'Заняття {when_label(lesson.start)} знову в розкладі.')
        if soon(lesson.start) and lesson.start > timezone.now():
            notify_student(lesson.student, f'📅 Заняття {when_label(lesson.start)} відбудеться.')
    return back_to_week(request, timezone.localtime(lesson.start).date())


@login_required
@require_POST
def schedule_done(request, lesson_id):
    """Заняття відбулося без звіту (наприклад, НМТ — там бал додають окремо)."""
    lesson = own_lesson(request, lesson_id)
    if lesson.status == 'planned' and lesson.start <= timezone.now():
        lesson.status = 'done'
        lesson.save(update_fields=['status'])
    return back_to_week(request, timezone.localtime(lesson.start).date())


@login_required
def schedule_report(request, lesson_id):
    """Звіт після заняття: учень, дата й тема вже підставлені, звіт одразу видно батькам."""
    lesson = own_lesson(request, lesson_id)
    local = timezone.localtime(lesson.start)
    if lesson.report_id:
        messages.info(request, 'Звіт до цього заняття вже є.')
        return redirect(week_url(local.date()))
    if not teachers.students_of(request.user).filter(id=lesson.student_id).exists():
        messages.error(request, 'Цей учень більше не у вашому списку — звіт не додати.')
        return redirect(week_url(local.date()))
    # Звіт за цей день уже написали (наприклад, після практики на уроці) — не дублюємо, а прив'язуємо
    written = StudentReport.objects.filter(student=lesson.student, date=local.date(), lesson__isnull=True).first()
    if written:
        attach_report(lesson, written)
        messages.info(request, f'Звіт за {local:%d.%m} для {lesson.student.real_name} уже є (його збережено раніше, '
                               f'наприклад після практики на уроці) — заняття позначено як проведене.')
        return redirect(reverse('cabinet') + '#teach' if request.GET.get('next') == 'cabinet'
                        else week_url(local.date()))
    topics = report_topics(request.user)
    if request.method == 'POST':
        form = StudentReportForm(request.POST)
        form.fields['curriculum_topic'].queryset = topics
        if form.is_valid():
            with transaction.atomic():
                report = form.save(commit=False)
                report.student = lesson.student
                report.date = local.date()
                report.save()
                attach_report(lesson, report)
            messages.success(request, f'✅ Звіт для {lesson.student.real_name} збережено — його вже видно батькам.')
            if request.POST.get('next') == 'cabinet':
                return redirect(reverse('cabinet') + '#teach')
            return redirect(week_url(local.date()))
    else:
        form = None
    previous = (StudentReport.objects.filter(student=lesson.student).select_related('curriculum_topic')
                .order_by('-date', '-id').first())
    # Як у звіті зі сторінки результатів: оцінки й тема — з практики на занятті, статус ДЗ — з останнього ДЗ
    attempt = lesson_practice(lesson)
    initial = {'nush_modeling': 10, 'nush_solving': 10, 'nush_analysis': 10, 'teacher_comment': '',
               'homework_status': homework.report_status(lesson.student) or 'completed',
               'curriculum_topic': lesson.curriculum_topic_id or (previous.curriculum_topic_id if previous else None)}
    if attempt:
        initial.update(nush_modeling=attempt.nush_modeling, nush_solving=attempt.nush_solving,
                       nush_analysis=attempt.nush_analysis)
        initial['curriculum_topic'] = attempt.material.curriculum_topic_id or initial['curriculum_topic']
    if form:
        initial.update({key: form.data.get(key) for key in initial if form.data.get(key)})
    initial['curriculum_topic'] = str(initial['curriculum_topic'] or '')
    return render(request, 'materials/schedule_report.html', {
        'lesson': annotate([lesson])[0], 'form': form, 'topics': topics, 'initial': initial, 'attempt': attempt,
        'hw_choices': StudentReport.HW_CHOICES,
        'previous': previous, 'summary_fields': StudentReport.summary_fields(),
        'back_url': week_url(local.date()), 'next': request.GET.get('next') or request.POST.get('next', ''),
    })
