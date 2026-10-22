"""Навчальний план учня: теми за деревом, які викладач міняє під учня (порядок, пропуск, теми з інших класів, власні
теми). Дерево тем при цьому не змінюється — план зберігається окремо для кожного учня (StudyPlanItem).

* Склад — кнопкою «Скласти з дерева»: теми класу учня («N клас» — усі шкільні курси класу; НМТ — курс НМТ) у порядку
  дерева. Теми, з яких уже є звіти заняття, одразу позначаються пройденими.
* Прогрес: звіт заняття з темою позначає тему пройденою (mark_reported); рівень — з останньої практики з теми.
* Розклад: наступним заняттям учня підставляються наступні теми плану (next_topics), звіт — так само.
* План бачать учень (кабінет) і батьки (їхня сторінка) — без приміток викладача."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F, Max
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from . import practice, teachers
from .models import (NMT_SUBJECT_NAME, CurriculumGrade, CurriculumTopic, PracticeAttempt, StudentReport,
                     StudyPlanItem, TutorStudentRequest)

TOPIC_ORDER = ('chapter__grade__subject__order', 'chapter__grade__order', 'chapter__order', 'order')


# ─── СКЛАД ПЛАНУ ─────────────────────────────────────────────
def class_grades(student):
    """Класи дерева для плану учня: «N клас» — усі шкільні курси класу (5–6 — математика, 7–11 — алгебра й
    геометрія), НМТ і «Закінчив школу» — курс НМТ."""
    grades = CurriculumGrade.objects.select_related('subject')
    if student.course.startswith('grade_'):
        return grades.filter(number=int(student.course.split('_')[1])).exclude(subject__name=NMT_SUBJECT_NAME)
    return grades.filter(subject__name=NMT_SUBJECT_NAME)


def available_grades(teacher):
    """Класи, з яких викладач може брати теми: власник — усі, репетитор — класи своєї підписки."""
    grades = CurriculumGrade.objects.select_related('subject').order_by('subject__order', 'order')
    licensed = teachers.licensed_grade_ids(teacher)
    return grades if licensed is None else grades.filter(id__in=licensed)


def append_topics(student, topics):
    """Додає теми в кінець плану (ті, що вже є в плані, пропускає); повертає кількість доданих."""
    reported = set(StudentReport.objects.filter(student=student).values_list('curriculum_topic_id', flat=True))
    present = set(student.plan_items.exclude(topic__isnull=True).values_list('topic_id', flat=True))
    position = (student.plan_items.aggregate(top=Max('position'))['top'] or 0)
    items = []
    for topic in topics:
        if topic.id in present:
            continue
        present.add(topic.id)
        position += 1
        done = topic.id in reported
        items.append(StudyPlanItem(student=student, topic=topic, position=position,
                                   status='done' if done else 'todo', done_on=timezone.localdate() if done else None))
    StudyPlanItem.objects.bulk_create(items)
    return len(items)


def grade_topics(grades):
    return CurriculumTopic.objects.filter(chapter__grade__in=grades).select_related('chapter__grade').order_by(
        *TOPIC_ORDER)


def renumber(student):
    items = list(student.plan_items.order_by('position', 'id'))
    for number, item in enumerate(items, start=1):
        item.position = number
    StudyPlanItem.objects.bulk_update(items, ['position'])
    return items


# ─── ПРОГРЕС ─────────────────────────────────────────────────
def mark_reported(student, topic):
    """Звіт заняття з темою — тема плану пройдена."""
    if topic is None:
        return
    student.plan_items.filter(topic=topic, status='todo').update(status='done', done_on=timezone.localdate())


def plan_items(student):
    """Теми плану з підписами: курс і розділ, рівень з останньої практики з теми."""
    items = list(student.plan_items.select_related('topic__chapter__grade__subject'))
    topic_ids = [item.topic_id for item in items if item.topic_id]
    levels = {}
    if topic_ids:
        for attempt in (PracticeAttempt.objects.filter(user_id=student.user_id,
                                                       material__curriculum_topic_id__in=topic_ids,
                                                       nush_modeling__isnull=False)
                        .only('material__curriculum_topic_id', 'nush_modeling', 'nush_solving', 'nush_analysis',
                              'created_at').select_related('material').order_by('created_at')):
            levels[attempt.material.curriculum_topic_id] = practice.level_name(practice.overall_grade(attempt))
    for item in items:
        item.level = levels.get(item.topic_id)
        item.place = (f'{item.topic.chapter.grade.short_label} · {item.topic.chapter.name}' if item.topic_id
                      else 'Власна тема')
    return items


def summary(items):
    counted = [item for item in items if item.status != 'skipped']
    done = sum(item.status == 'done' for item in counted)
    return {'done': done, 'total': len(counted), 'percent': round(100 * done / len(counted)) if counted else 0,
            'next': [item for item in items if item.status == 'todo'][:3]}


def next_topics(student_ids):
    """{id учня: [теми плану, що чекають, по порядку]} — для розкладу й звіту."""
    upcoming = {}
    for item in (StudyPlanItem.objects.filter(student_id__in=student_ids, status='todo')
                 .select_related('topic').order_by('position', 'id')):
        upcoming.setdefault(item.student_id, []).append(item)
    return upcoming


def student_view(student):
    """План для учня й батьків — без приміток викладача; None, якщо плану немає."""
    items = plan_items(student)
    if not items:
        return None
    for item in items:
        item.note = ''
    return {'items': items, **summary(items)}


# ─── СТОРІНКА ПЛАНУ (ВИКЛАДАЧ) ───────────────────────────────
def own_student(request, student_id):
    if not teachers.is_tutor(request.user):
        raise Http404
    return get_object_or_404(teachers.students_of(request.user), id=student_id)


def allowed_topic(teacher, topic_id):
    topic_id = int(topic_id) if str(topic_id).isdigit() else 0
    return CurriculumTopic.objects.filter(
        id=topic_id, chapter__grade__in=available_grades(teacher)).select_related('chapter__grade').first()


@login_required
def plan_page(request, student_id):
    student = own_student(request, student_id)
    items = plan_items(student)
    grades = list(available_grades(request.user))
    own = set(class_grades(student).values_list('id', flat=True))
    for grade in grades:
        grade.is_own = grade.id in own
    topics = grade_topics(grades)
    return render(request, 'materials/study_plan.html', {
        'student': student, 'items': items, 'summary': summary(items), 'grades': grades,
        'topic_groups': [(grade, [t for t in topics if t.chapter.grade_id == grade.id]) for grade in grades],
        'status_choices': StudyPlanItem.STATUS_CHOICES,
    })


def back(student, anchor=''):
    return redirect(reverse('study_plan', args=[student.id]) + anchor)


@login_required
@require_POST
def plan_build(request, student_id):
    """Скласти план з дерева (порожній план) або додати теми ще одного класу в кінець."""
    student = own_student(request, student_id)
    ids = [int(value) for value in request.POST.getlist('grade') if value.isdigit()]
    grades = available_grades(request.user).filter(id__in=ids)
    if not grades:
        messages.error(request, 'Оберіть хоча б один курс і клас.')
        return back(student)
    with transaction.atomic():
        if request.POST.get('replace') == '1':
            student.plan_items.all().delete()
        added = append_topics(student, grade_topics(grades))
    messages.success(request, f'✅ До плану {student.real_name} додано тем: {added}.' if added
                     else 'Усі теми цих класів уже є в плані.')
    return back(student)


@login_required
@require_POST
def plan_add(request, student_id):
    """Одна тема з дерева (будь-якого доступного класу) або власна тема — в кінець плану чи одразу після
    наступної теми."""
    student = own_student(request, student_id)
    topic = allowed_topic(request.user, request.POST.get('topic_id', ''))
    title = request.POST.get('title', '').strip()[:255]
    if not topic and not title:
        messages.error(request, 'Оберіть тему з дерева або напишіть власну.')
        return back(student)
    if topic and student.plan_items.filter(topic=topic).exists():
        messages.info(request, f'Тема «{topic.name}» уже є в плані.')
        return back(student)
    with transaction.atomic():
        items = renumber(student)
        if request.POST.get('where') == 'next':
            first_todo = next((item for item in items if item.status == 'todo'), None)
            position = first_todo.position if first_todo else len(items) + 1
            student.plan_items.filter(position__gte=position).update(position=F('position') + 1)
        else:
            position = len(items) + 1
        StudyPlanItem.objects.create(student=student, topic=topic, title='' if topic else title, position=position,
                                     note=request.POST.get('note', '').strip()[:300])
    messages.success(request, f'✅ Тему «{topic.name if topic else title}» додано до плану.')
    return back(student)


def own_item(request, item_id):
    if not teachers.is_tutor(request.user):
        raise Http404
    return get_object_or_404(StudyPlanItem.objects.select_related('student', 'topic'), id=item_id,
                             student__in=teachers.students_of(request.user))


@login_required
@require_POST
def plan_item_update(request, item_id):
    """Дії з темою: стан (пройдено / пропущено / за планом), примітка, вгору / вниз / на позицію, видалити."""
    item = own_item(request, item_id)
    student = item.student
    action = request.POST.get('action', '')
    anchor = f'#item-{item.id}'
    if action == 'status' and request.POST.get('status') in dict(StudyPlanItem.STATUS_CHOICES):
        item.status = request.POST['status']
        item.done_on = timezone.localdate() if item.status == 'done' else None
        item.save(update_fields=['status', 'done_on'])
    elif action == 'note':
        item.note = request.POST.get('note', '').strip()[:300]
        item.save(update_fields=['note'])
    elif action == 'delete':
        item.delete()
        renumber(student)
        anchor = ''
    elif action in ('up', 'down', 'move'):
        with transaction.atomic():
            items = renumber(student)
            index = next(i for i, other in enumerate(items) if other.id == item.id)
            if action == 'move':
                target = request.POST.get('position', '')
                target = int(target) - 1 if target.isdigit() else index
            else:
                target = index - 1 if action == 'up' else index + 1
            target = max(0, min(len(items) - 1, target))
            items.insert(target, items.pop(index))
            for number, other in enumerate(items, start=1):
                other.position = number
            StudyPlanItem.objects.bulk_update(items, ['position'])
    return back(student, anchor)


@login_required
@require_POST
def plan_clear(request, student_id):
    student = own_student(request, student_id)
    student.plan_items.all().delete()
    messages.info(request, f'План {student.real_name} очищено.')
    return back(student)
