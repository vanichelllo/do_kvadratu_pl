"""«Що підготувати»: які уроки (презентації й банки завдань) потрібні найближчим часом — за розкладом занять і
навчальними планами учнів. Лише для власника сайту: уроки платформи готує він.

Для кожного майбутнього заняття (за WEEKS тижнів) — його тема: задана в занятті або наступна за планом учня (по
черзі, як у розкладі; об'єднані теми — усі). Тема готова, коли на сайті є презентація й завдання для практики;
інакше — у списку, раніше потрібні — вище. Підказка, куди класти файли уроку, — як у CLAUDE.md:
content/school/<папка>/<номер>.html і bank_<номер>.py (папка — за meta.json)."""
import datetime
import json
import re
from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from . import plans, schedule, teachers
from .models import NMT_SUBJECT_NAME, Lesson, LessonSeries, Question, StudyMaterial

WEEKS = 4
MIN_QUESTIONS = 9      # менше — практика сходинками бідна (по 3 рівні × 3 навички)
SUBJECT_FOLDERS = (('Математика', 'math'), ('Алгебра', 'algebra'), ('Геометрія', 'geometry'))


def content_folders():
    """{(курс, клас): назва папки} — з meta.json у content/school."""
    folders = {}
    for meta in (Path(settings.BASE_DIR) / 'content' / 'school').glob('*/meta.json'):
        try:
            data = json.loads(meta.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            continue
        folders[(data.get('course'), data.get('grade'))] = meta.parent.name
    return folders


def topic_files(topic, folders):
    """(папка, файл презентації, файл банку) для теми шкільного курсу; None для НМТ і діагностики."""
    grade = topic.chapter.grade
    if grade.subject.name == NMT_SUBJECT_NAME or topic.kind == 'diagnostic':
        return None
    folder = folders.get((grade.subject.name, grade.name))
    if not folder:
        prefix = next((p for word, p in SUBJECT_FOLDERS if grade.subject.name.startswith(word)), 'math')
        folder = f'{prefix}-{grade.number}'
    if topic.kind == 'summary':
        chapter = re.match(r'Розділ (\d+)', topic.chapter.name)
        return (folder, f'summary-{chapter.group(1)}.html', None) if chapter else None
    number = topic.name.split('. ')[0]
    return folder, f'{number}.html', f'bank_{number}.py'


def needed_topics(until):
    """[(заняття, [теми])] — майбутні заплановані заняття до until і їхні теми (з заняття або з плану учня)."""
    lessons = list(Lesson.objects.filter(status='planned', start__gte=timezone.now(), start__lt=until)
                   .select_related('student', 'curriculum_topic__chapter__grade__subject').order_by('start'))
    slots = plans.next_slot_topics({lesson.student_id for lesson in lessons})
    queue, result = {}, []
    for lesson in lessons:
        if lesson.curriculum_topic_id:
            result.append((lesson, [lesson.curriculum_topic]))
            continue
        index = queue.get(lesson.student_id, 0)
        queue[lesson.student_id] = index + 1
        student_slots = slots.get(lesson.student_id, [])
        result.append((lesson, student_slots[index] if index < len(student_slots) else []))
    return result


def readiness(topics):
    """{id теми: {'presentation': bool, 'questions': int}} — що вже є на сайті."""
    ids = [topic.id for topic in topics]
    with_html = set(StudyMaterial.objects.filter(curriculum_topic_id__in=ids, is_bundle=False)
                    .exclude(Q(html_content__isnull=True) | Q(html_content=''))
                    .values_list('curriculum_topic_id', flat=True))
    counts = dict(Question.objects.filter(curriculum_topic_id__in=ids).values('curriculum_topic_id')
                  .annotate(n=Count('id')).values_list('curriculum_topic_id', 'n'))
    return {topic_id: {'presentation': topic_id in with_html, 'questions': counts.get(topic_id, 0)} for topic_id in ids}


def priorities(weeks=WEEKS):
    """Теми, потрібні за розкладом найближчі weeks тижнів: спершу неготові (раніше потрібні — вище), потім готові.
    Плюс заняття без теми (у учня немає плану або план закінчився)."""
    today = timezone.localdate()
    until = schedule.aware(today + datetime.timedelta(weeks=weeks), datetime.time.min)
    schedule.fill_series(LessonSeries.objects.all(), until=today + datetime.timedelta(weeks=weeks))
    rows, without_topic = {}, []
    for lesson, topics in needed_topics(until):
        if not topics:
            without_topic.append(lesson)
        for topic in topics:
            row = rows.setdefault(topic.id, {'topic': topic, 'lessons': []})
            row['lessons'].append(lesson)
    status = readiness([row['topic'] for row in rows.values()])
    folders = content_folders()
    content_root = Path(settings.BASE_DIR) / 'content' / 'school'
    for row in rows.values():
        topic = row['topic']
        info = status[topic.id]
        row['first'] = timezone.localtime(row['lessons'][0].start)
        row['days'] = (row['first'].date() - today).days
        row['students'] = []
        for lesson in row['lessons']:
            if lesson.student.real_name not in row['students']:
                row['students'].append(lesson.student.real_name)
        row['presentation'] = info['presentation']
        row['questions'] = info['questions']
        files = topic_files(topic, folders)
        row['special'] = topic.kind != 'lesson'
        row['nmt'] = topic.chapter.grade.subject.name == NMT_SUBJECT_NAME
        row['file'] = row['bank_file'] = None
        row['file_in_repo'] = row['bank_in_repo'] = False
        if files:
            folder, html_name, bank_name = files
            row['file'] = f'content/school/{folder}/{html_name}'
            row['bank_file'] = f'content/school/{folder}/{bank_name}' if bank_name else None
            row['file_in_repo'] = (content_root / folder / html_name).exists()
            row['bank_in_repo'] = bool(bank_name) and (content_root / folder / bank_name).exists()
        needs_questions = not row['special'] and row['questions'] < MIN_QUESTIONS
        row['missing'] = (not row['presentation'] and topic.kind != 'diagnostic') or needs_questions
        row['few_questions'] = needs_questions and row['questions'] > 0
        # Файл уже в репозиторії, але на сайті ще немає — з'явиться після деплою
        row['awaiting_deploy'] = ((row['file_in_repo'] and not row['presentation'])
                                  or (row['bank_in_repo'] and needs_questions))
    ordered = sorted(rows.values(), key=lambda row: row['first'])
    return {'todo': [row for row in ordered if row['missing']], 'ready': [row for row in ordered if not row['missing']],
            'without_topic': without_topic, 'weeks': weeks}


def lesson_request(row):
    """«Зроби урок 6 клас, 2.4» — як просити Claude підготувати урок (CLAUDE.md)."""
    topic = row['topic']
    return f'Зроби урок {topic.chapter.grade.short_label}, {topic.name}'


@login_required
def prep_page(request):
    if not teachers.is_owner(request.user):
        return redirect('cabinet')
    weeks = request.GET.get('weeks', '')
    weeks = max(1, min(12, int(weeks))) if weeks.isdigit() else WEEKS
    context = priorities(weeks)
    for row in context['todo'] + context['ready']:
        row['request'] = lesson_request(row)
    context['requests'] = '\n'.join(row['request'] for row in context['todo'] if not row['nmt'])
    context['min_questions'] = MIN_QUESTIONS
    context['week_choices'] = (2, 4, 8)
    if request.GET.get('format') == 'txt':
        response = HttpResponse(as_text(context), content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="prep-{timezone.localdate():%Y-%m-%d}.txt"'
        return response
    return render(request, 'materials/schedule_prep.html', context)


def as_text(context):
    """Пріоритети підготовки — текстом (файл для завантаження)."""
    def when(row):
        days = row['days']
        return {0: 'сьогодні', 1: 'завтра'}.get(days, f'через {days} дн.')

    lines = [f'ЩО ПІДГОТУВАТИ — {timezone.localdate():%d.%m.%Y}, на {context["weeks"]} тиж.', '',
             f'НЕГОТОВІ ТЕМИ ({len(context["todo"])}) — за датою заняття', '']
    for number, row in enumerate(context['todo'], 1):
        topic = row['topic']
        lines.append(f'{number}. {row["first"]:%d.%m} ({when(row)}) — {topic.chapter.grade.short_label}: {topic.name}')
        missing = []
        if not row['presentation'] and topic.kind != 'diagnostic':
            missing.append('немає презентації')
        if not row['special'] and row['questions'] < context['min_questions']:
            missing.append(f'мало завдань ({row["questions"]})' if row['questions'] else 'немає завдань')
        if row['awaiting_deploy']:
            missing.append('файл уже в репозиторії — чекає деплою')
        lines.append(f'   {"; ".join(missing)}')
        lines.append(f'   учні: {", ".join(row["students"])} · занять: {len(row["lessons"])}')
        if row['file']:
            lines.append(f'   файли: {row["file"]}' + (f', {row["bank_file"]}' if row['bank_file'] else ''))
        lines.append('')
    if not context['todo']:
        lines += ['Усе готово.', '']
    if context['requests']:
        lines += ['ЗАПИТИ ДЛЯ CLAUDE (у порядку пріоритету)', '', context['requests'], '']
    if context['without_topic']:
        lines += ['ЗАНЯТТЯ БЕЗ ТЕМИ (план учня порожній або закінчився)', '']
        lines += [f'- {lesson.student.real_name} — {timezone.localtime(lesson.start):%d.%m %H:%M}'
                  for lesson in context['without_topic']]
        lines.append('')
    if context['ready']:
        lines += [f'ГОТОВІ ТЕМИ ({len(context["ready"])})', '']
        lines += [f'- {row["first"]:%d.%m} — {row["topic"].chapter.grade.short_label}: {row["topic"].name}'
                  f' ({", ".join(row["students"])})' for row in context['ready']]
    return '\n'.join(lines) + '\n'
