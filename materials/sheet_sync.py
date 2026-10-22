"""Зв'язок розкладу на сайті з Google-таблицею власника (вкладка «Розклад уроків»).

Головний розклад — на сайті. Таблиця раз на годину бере його за особистим посиланням (schedule_export, JSON) і
оновлює свої рядки: нові заняття, перенесення, скасування, тему зі звіту (tools/schedule_sheet_sync.gs). Ціни,
податки й оплату таблиця веде сама — сайт їх не знає й не чіпає.

Перехід: один раз імпортувати майбутні уроки з таблиці (CSV вкладки, рядки «Ще рано») — import_rows. Регулярні
уроки учня (той самий день тижня, час і тривалість) стають постійним заняттям, решта — разовими. Дати серії, яких
у таблиці немає (канікули), позначаються скасованими. Учень з таблиці зіставляється з учнем сайту за іменем;
ім'я з таблиці запам'ятовується (TutorStudentRequest.sheet_name), і таблиця далі отримує саме його."""
import csv
import datetime
import io
import re
from collections import Counter, defaultdict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import constant_time_compare

from . import schedule, teachers
from .models import Lesson, LessonSeries

UPCOMING = 'Ще рано'          # статус майбутнього уроку в таблиці
EXPORT_BACK = datetime.timedelta(days=14)
MAX_UPLOAD = 2 * 1024 * 1024
SERIES_MIN = 2                # стільки однакових уроків (день, час, тривалість) — уже постійне заняття
GAP_REASON = 'Немає в таблиці (канікули?)'


# ─── ВИВАНТАЖЕННЯ ДЛЯ ТАБЛИЦІ ────────────────────────────────
def lesson_row(lesson):
    start, end = timezone.localtime(lesson.start), timezone.localtime(lesson.end)
    topic = lesson.report.curriculum_topic if lesson.report_id and lesson.report.curriculum_topic_id else (
        lesson.curriculum_topic)
    moved = timezone.localtime(lesson.moved_from) if lesson.moved_from else None
    return {
        'id': lesson.id, 'starts_at': lesson.start.isoformat(),
        'name': lesson.student.sheet_name or lesson.student.real_name,
        'date': f'{start:%d.%m.%Y}', 'weekday': start.isoweekday(), 'start': f'{start:%H:%M:%S}',
        'end_date': f'{end:%d.%m.%Y}', 'end': f'{end:%H:%M:%S}', 'duration': lesson.duration,
        'status': lesson.status, 'reason': lesson.cancel_reason,
        'moved_from': f'{moved:%d.%m.%Y %H:%M}' if moved else '',
        'topic': topic.name if topic else '',
        'updated_at': lesson.updated_at.isoformat(),
    }


def schedule_export(request, token):
    """Розклад викладача для Google-таблиці: заняття від 2 тижнів тому до FILL_WEEKS наперед."""
    head = token.partition('-')[0]
    if head[:1] != 't' or not head[1:].isdigit() or not constant_time_compare(
            schedule.feed_token('t', int(head[1:])), token):
        raise Http404
    teacher_id = int(head[1:])
    today = timezone.localdate()
    until = today + datetime.timedelta(weeks=schedule.FILL_WEEKS)
    schedule.fill_series(LessonSeries.objects.filter(teacher_id=teacher_id), until=until)
    since = today - EXPORT_BACK
    lessons = (Lesson.objects.filter(teacher_id=teacher_id, start__gte=schedule.aware(since, datetime.time.min),
                                     start__lt=schedule.aware(until + datetime.timedelta(days=1), datetime.time.min))
               .select_related('student', 'curriculum_topic', 'report__curriculum_topic').order_by('start'))
    response = JsonResponse({'from': f'{since:%d.%m.%Y}', 'to': f'{until:%d.%m.%Y}',
                             'generated_at': timezone.now().isoformat(),
                             'lessons': [lesson_row(lesson) for lesson in lessons]},
                            json_dumps_params={'ensure_ascii': False})
    response['Cache-Control'] = 'private, no-store'
    response['X-Robots-Tag'] = 'noindex'
    return response


def export_url(user):
    return settings.SITE_URL + reverse('schedule_export', args=[schedule.feed_token('t', user.id)])


# ─── ІМПОРТ З ТАБЛИЦІ ────────────────────────────────────────
def normalize(name):
    return re.sub(r'\s+', ' ', name or '').strip().casefold()


def parse_time(value):
    match = re.match(r'^\s*(\d{1,2}):(\d{2})', value or '')
    if not match or int(match[1]) > 23 or int(match[2]) > 59:
        return None
    return datetime.time(int(match[1]), int(match[2]))


def parse_date(value):
    try:
        return datetime.datetime.strptime((value or '').strip(), '%d.%m.%Y').date()
    except ValueError:
        return None


def read_rows(text, today):
    """Майбутні уроки з CSV вкладки «Розклад уроків»: [{name, date, time, duration, line}] і список помилок."""
    reader = csv.DictReader(io.StringIO(text.lstrip('﻿')))
    needed = {'Student', 'Start date', 'Start time', 'Status1'}
    if not reader.fieldnames or not needed <= set(reader.fieldnames):
        return [], ['У файлі немає стовпців Student, Start date, Start time, Status1 — це точно CSV вкладки '
                    '«Розклад уроків»?']
    rows, errors = [], []
    for line, raw in enumerate(reader, start=2):
        if (raw.get('Status1') or '').strip() != UPCOMING:
            continue
        day, start = parse_date(raw.get('Start date')), parse_time(raw.get('Start time'))
        name = (raw.get('Student') or '').strip()
        if not (day and start and name):
            errors.append(f'Рядок {line}: не вдалося прочитати учня, дату чи час — пропущено.')
            continue
        if day < today:
            continue
        end = parse_time(raw.get('End time'))
        minutes = (end.hour * 60 + end.minute) - (start.hour * 60 + start.minute) if end else 0
        rows.append({'name': name, 'date': day, 'time': start, 'line': line,
                     'duration': minutes if 15 <= minutes <= 240 else None})
    return rows, errors


def auto_match(name, students):
    """Учень сайту для імені з таблиці: точний збіг (ім'я з таблиці чи справжнє), інакше — єдиний учень, чиє ім'я
    починається з цього («Олексій» → «Олексій Шевцов»); None, якщо не знайдено або неоднозначно."""
    key = normalize(name)
    exact = [s for s in students if key in (normalize(s.sheet_name), normalize(s.real_name))]
    if len(exact) == 1:
        return exact[0]
    prefix = [s for s in students if normalize(s.real_name).startswith(key + ' ')
              or normalize(s.real_name).split(' ')[-1:] == [key]]
    return prefix[0] if len(prefix) == 1 else None


def plan_import(rows):
    """{ім'я: {'series': [(weekday, time, duration, [дати])], 'single': [(дата, час, тривалість)]}}."""
    by_name = defaultdict(list)
    for row in rows:
        by_name[row['name']].append(row)
    plan = {}
    for name, items in by_name.items():
        durations = Counter(row['duration'] for row in items if row['duration'])
        usual = durations.most_common(1)[0][0] if durations else 60
        groups = defaultdict(list)
        for row in items:
            groups[(row['date'].weekday(), row['time'], row['duration'] or usual)].append(row['date'])
        series, single = [], []
        for (weekday, time, duration), dates in sorted(groups.items(), key=lambda g: (g[0][0], g[0][1])):
            dates = sorted(set(dates))
            if len(dates) >= SERIES_MIN:
                series.append((weekday, time, duration, dates))
            else:
                single += [(day, time, duration) for day in dates]
        plan[name] = {'series': series, 'single': sorted(single)}
    return plan


def plan_labels(parts):
    """«🔁 щопонеділка о 16:00, 50 хв — 12 уроків (26.10–24.05)», «📅 03.11 о 17:00» — для перегляду."""
    labels = [f'🔁 {schedule.WEEKDAYS_EVERY[weekday]} о {time:%H:%M}, {duration} хв — уроків: {len(dates)} '
              f'({dates[0]:%d.%m}–{dates[-1]:%d.%m})' for weekday, time, duration, dates in parts['series']]
    return labels + [f'📅 {day:%d.%m} о {time:%H:%M}' for day, time, _ in parts['single']]


def import_rows(teacher, plan, mapping):
    """Створює заняття за планом імпорту; mapping — {ім'я з таблиці: учень}. Те, що вже є на сайті (заняття
    учня в той самий час, постійне з тим самим днем і часом), пропускає. Повертає лічильники."""
    counts = Counter()
    for name, parts in plan.items():
        student = mapping.get(name)
        if student is None:
            continue
        if student.sheet_name != name:
            student.sheet_name = name
            student.save(update_fields=['sheet_name'])
        for weekday, time, duration, dates in parts['series']:
            if LessonSeries.objects.filter(teacher=teacher, student=student, weekday=weekday, time=time).filter(
                    Q(ends_on__isnull=True) | Q(ends_on__gte=dates[0])).exists():
                counts['skipped'] += len(dates)
                continue
            series = LessonSeries.objects.create(teacher=teacher, student=student, weekday=weekday, time=time,
                                                 duration=duration, starts_on=dates[0], ends_on=dates[-1])
            schedule.fill_series(LessonSeries.objects.filter(id=series.id), until=dates[-1])
            gaps = series.lessons.exclude(series_date__in=dates)
            counts['gaps'] += gaps.update(status='cancelled', cancel_reason=GAP_REASON)
            counts['series'] += 1
            counts['lessons'] += len(dates)
        for day, time, duration in parts['single']:
            start = schedule.aware(day, time)
            if Lesson.objects.filter(student=student, start=start).exists():
                counts['skipped'] += 1
                continue
            Lesson.objects.create(teacher=teacher, student=student, start=start, duration=duration)
            counts['single'] += 1
            counts['lessons'] += 1
    return counts


@login_required
def schedule_import(request):
    """Імпорт майбутніх уроків з CSV вкладки «Розклад уроків»: спершу перегляд (хто кому відповідає, скільки
    постійних і разових занять), потім — імпорт."""
    if not teachers.is_tutor(request.user):
        return redirect('cabinet')
    students = list(teachers.students_of(request.user).order_by('real_name'))
    context = {'students': students, 'export_url': export_url(request.user)}
    if request.method != 'POST':
        return render(request, 'materials/schedule_import.html', context)

    upload = request.FILES.get('file')
    if upload:
        if upload.size > MAX_UPLOAD:
            messages.error(request, 'Файл завеликий — потрібен CSV лише вкладки «Розклад уроків».')
            return redirect('schedule_import')
        text = upload.read().decode('utf-8', errors='replace')
    else:
        text = request.POST.get('csv', '')
    rows, errors = read_rows(text, timezone.localdate())
    plan = plan_import(rows)
    by_id = {str(s.id): s for s in students}
    names = sorted(plan)
    mapping = {}
    for index, name in enumerate(names):
        chosen = request.POST.get(f'map_{index}')
        mapping[name] = by_id.get(chosen) if chosen is not None else auto_match(name, students)

    if request.POST.get('confirm') == '1' and rows:
        with transaction.atomic():
            counts = import_rows(request.user, plan, mapping)
        messages.success(request, f"✅ Імпортовано уроків: {counts['lessons']} (постійних занять — {counts['series']}, "
                                  f"разових — {counts['single']}). Дати без уроку в таблиці позначено скасованими: "
                                  f"{counts['gaps']}. Уже були на сайті й пропущені: {counts['skipped']}.")
        return redirect('schedule')

    context.update({
        'preview': True, 'csv': text, 'errors': errors, 'rows_count': len(rows),
        'names': [{'index': index, 'name': name, 'student': mapping[name], 'labels': plan_labels(plan[name]),
                   'count': sum(len(s[3]) for s in plan[name]['series']) + len(plan[name]['single'])}
                  for index, name in enumerate(names)],
    })
    return render(request, 'materials/schedule_import.html', context)


@login_required
def sheet_script(request):
    """Скрипт для Google-таблиці (tools/schedule_sheet_sync.gs) — відкрити й скопіювати в Apps Script."""
    if not teachers.is_tutor(request.user):
        raise Http404
    code = (settings.BASE_DIR / 'tools' / 'schedule_sheet_sync.gs').read_text(encoding='utf-8')
    return HttpResponse(code, content_type='text/plain; charset=utf-8')
