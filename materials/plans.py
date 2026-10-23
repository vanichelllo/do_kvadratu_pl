"""Навчальний план учня: теми за деревом, які викладач міняє під учня (порядок, пропуск, теми з інших класів, власні
теми). Дерево тем при цьому не змінюється — план зберігається окремо для кожного учня (StudyPlanItem).

* Склад — кнопкою «Скласти з дерева»: теми класу учня («N клас» — усі шкільні курси класу; НМТ — алгебра й
  геометрія НМТ окремими курсами) у порядку дерева, курси можна чергувати й починати з певної теми. Теми, з яких уже є звіти заняття, одразу позначаються пройденими.
* Під учня: тема на кілька уроків (lessons), дві-три теми одним уроком (joined — разом з попередньою), повторення
  пройденої теми пізніше (копія теми в плані), «Пропустити» — тему не проводять.
* Прогрес: звіт заняття з темою — проведено урок цієї теми (mark_reported); тема пройдена, коли проведено всі її
  уроки. Рівень — з останньої практики з теми.
* Розклад: наступним заняттям учня підставляються наступні уроки плану (next_slots), звіт — так само.
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


# Курс НМТ у дереві — один «клас» без поділу на алгебру й геометрію; на заняттях їх чергують, тож у плані
# він — два курси. Геометрія НМТ — розділи з такими назвами (решта — алгебра).
NMT_GEOMETRY_CHAPTERS = ('Планіметрія', 'Стереометрія', 'Координати та вектори')


class Course:
    """Курс для складання плану: клас дерева або частина класу НМТ (алгебра / геометрія). key — значення у формі."""

    def __init__(self, key, label, grade, topics):
        self.key, self.label, self.grade, self.topics = key, label, grade, topics
        self.is_own = False


def is_nmt_geometry(topic):
    return any(name in topic.chapter.name for name in NMT_GEOMETRY_CHAPTERS)


def plan_courses(grades):
    """Курси для форми плану в порядку дерева: кожен шкільний клас — курс, НМТ — «НМТ · Алгебра» і «НМТ · Геометрія»."""
    grades = list(grades)
    topics = list(grade_topics(grades))
    courses = []
    for grade in grades:
        own = [t for t in topics if t.chapter.grade_id == grade.id]
        if grade.subject.name != NMT_SUBJECT_NAME:
            courses.append(Course(str(grade.id), grade.short_label, grade, own))
            continue
        algebra = [t for t in own if not is_nmt_geometry(t)]
        geometry = [t for t in own if is_nmt_geometry(t)]
        if not geometry:
            courses.append(Course(str(grade.id), grade.short_label, grade, own))
            continue
        courses.append(Course(f'{grade.id}a', 'НМТ · Алгебра', grade, algebra))
        courses.append(Course(f'{grade.id}g', 'НМТ · Геометрія', grade, geometry))
    return courses


def course_topics(courses, starts=None, alternate=False, first=None):
    """Теми обраних курсів для плану. starts — {курс: id теми}: з якої теми починати цей курс (попередні теми курсу
    в план не потрапляють). alternate — чергувати курси (алгебра, геометрія, алгебра…), інакше — курс за курсом.
    first — курс, з якого план починається (інакше — порядок дерева)."""
    starts = starts or {}
    lists = []
    for course in sorted(courses, key=lambda c: c.key != first):   # sorted стабільний: решта — у порядку дерева
        topics = course.topics
        start = next((i for i, t in enumerate(topics) if t.id == starts.get(course.key)), 0)
        lists.append(topics[start:])
    if not alternate:
        return [topic for topics in lists for topic in topics]
    merged = []
    for index in range(max((len(topics) for topics in lists), default=0)):
        merged += [topics[index] for topics in lists if index < len(topics)]
    return merged


def renumber(student):
    items = list(student.plan_items.order_by('position', 'id'))
    for number, item in enumerate(items, start=1):
        item.position = number
    StudyPlanItem.objects.bulk_update(items, ['position'])
    return items


# ─── ПРОГРЕС ─────────────────────────────────────────────────
# Тема плану може йти кілька уроків (lessons) і бути об'єднаною з попередньою темою в один урок (joined).
# Урок плану — група тем, з'єднаних joined, і він повторюється стільки разів, скільки уроків лишилося.
def group_items(items):
    """Сусідні теми, з'єднані joined, — одна група (один урок)."""
    groups = []
    for item in items:
        if item.joined and groups:
            groups[-1].append(item)
        else:
            groups.append([item])
    return groups


def mark_reported(student, topic):
    """Звіт заняття з темою — проведено урок першої теми плану з нею, що чекає, і тем, об'єднаних з нею в
    один урок; тема пройдена, коли проведено всі її уроки."""
    if topic is None:
        return
    items = list(student.plan_items.order_by('position', 'id'))
    group = next((group for group in group_items(items)
                  if any(item.topic_id == topic.id and item.status == 'todo' for item in group)), None)
    for item in group or []:
        if item.status != 'todo':
            continue
        item.held += 1
        if item.held >= item.lessons:
            item.status, item.done_on = 'done', timezone.localdate()
        item.save(update_fields=['held', 'status', 'done_on'])


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


def lesson_slots(items):
    """Уроки, що чекають, по порядку: [(назва уроку, перша тема з дерева, теми групи)]. Тема на 3 уроки, з якої
    проведено 1, дає 2 уроки; об'єднані теми — один урок «1.4 + 1.5»."""
    slots = []
    for group in group_items(items):
        todo = [item for item in group if item.status == 'todo']
        if not todo:
            continue
        name = ' + '.join(item.name for item in todo)
        topic_id = next((item.topic_id for item in todo if item.topic_id), None)
        slots += [(name, topic_id, todo)] * max(1, max(item.lessons - item.held for item in todo))
    return slots


def summary(items):
    counted = [item for item in items if item.status != 'skipped']
    done = sum(item.status == 'done' for item in counted)
    upcoming = []
    for name, _, group in lesson_slots(items):
        if group[0] not in [g[0] for _, g in upcoming]:
            group[0].slot_name = name
            upcoming.append((name, group))
    return {'done': done, 'total': len(counted), 'percent': round(100 * done / len(counted)) if counted else 0,
            'next': [group[0] for _, group in upcoming[:3]]}


def next_slots(student_ids):
    """{id учня: [(назва уроку, тема з дерева), ...]} — уроки плану, що чекають, для розкладу й звіту."""
    by_student = {}
    for item in (StudyPlanItem.objects.filter(student_id__in=student_ids)
                 .exclude(status='skipped').select_related('topic').order_by('position', 'id')):
        by_student.setdefault(item.student_id, []).append(item)
    return {student_id: [(name, topic_id) for name, topic_id, _ in lesson_slots(items)]
            for student_id, items in by_student.items()}


def next_slot_topics(student_ids):
    """{id учня: [[теми дерева уроку], ...]} — наступні уроки плану з усіма темами (об'єднані — разом), по черзі."""
    by_student = {}
    for item in (StudyPlanItem.objects.filter(student_id__in=student_ids).exclude(status='skipped')
                 .select_related('topic__chapter__grade__subject').order_by('position', 'id')):
        by_student.setdefault(item.student_id, []).append(item)
    return {student_id: [[item.topic for item in group if item.topic_id] for _, _, group in lesson_slots(items)]
            for student_id, items in by_student.items()}


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
    courses = plan_courses(grades)
    for course in courses:
        course.is_own = course.grade.id in own
    topics = grade_topics(grades)
    return render(request, 'materials/study_plan.html', {
        'student': student, 'items': items, 'summary': summary(items), 'courses': courses,
        'topic_groups': [(grade, [t for t in topics if t.chapter.grade_id == grade.id]) for grade in grades],
        'own_courses': sum(course.is_own for course in courses),
        'status_choices': StudyPlanItem.STATUS_CHOICES,
    })


def back(student, anchor=''):
    return redirect(reverse('study_plan', args=[student.id]) + anchor)


@login_required
@require_POST
def plan_build(request, student_id):
    """Скласти план з дерева (порожній план) або додати теми ще одного класу в кінець; курси можна чергувати й
    починати кожен з певної теми."""
    student = own_student(request, student_id)
    keys = request.POST.getlist('grade')
    chosen = [course for course in plan_courses(available_grades(request.user)) if course.key in keys]
    if not chosen:
        messages.error(request, 'Оберіть хоча б один курс і клас.')
        return back(student)
    starts = {course.key: int(value) for course in chosen
              if (value := request.POST.get(f'start_{course.key}', '')).isdigit()}
    topics = course_topics(chosen, starts, alternate=request.POST.get('alternate') == '1',
                           first=request.POST.get('first') or None)
    with transaction.atomic():
        if request.POST.get('replace') == '1':
            student.plan_items.all().delete()
        added = append_topics(student, topics)
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
    again = bool(topic and student.plan_items.filter(topic=topic).exists())
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
    messages.success(request, f'✅ Тему «{topic.name if topic else title}» додано до плану'
                              + (' ще раз — для повторення.' if again else '.'))
    return back(student)


def own_item(request, item_id):
    if not teachers.is_tutor(request.user):
        raise Http404
    return get_object_or_404(StudyPlanItem.objects.select_related('student', 'topic'), id=item_id,
                             student__in=teachers.students_of(request.user))


MAX_LESSONS = 10


def unjoin_next(student, item):
    """Тема, об'єднана з item, після переміщення чи видалення item більше ні до чого не прив'язана."""
    following = student.plan_items.filter(position__gt=item.position).order_by('position', 'id').first()
    if following and following.joined:
        following.joined = False
        following.save(update_fields=['joined'])


@login_required
@require_POST
def plan_item_update(request, item_id):
    """Дії з темою: стан (пройдено / пропущено / за планом), кількість уроків, разом з попередньою (один урок),
    почати звідси, повторити пізніше, примітка, вгору / вниз / на позицію, видалити."""
    item = own_item(request, item_id)
    student = item.student
    action = request.POST.get('action', '')
    anchor = f'#item-{item.id}'
    if action == 'status' and request.POST.get('status') in dict(StudyPlanItem.STATUS_CHOICES):
        if item.status == 'done' and request.POST['status'] == 'todo':
            item.held = 0   # повернули пройдену тему в план — її уроки рахуються заново
        item.status = request.POST['status']
        item.done_on = timezone.localdate() if item.status == 'done' else None
        item.save(update_fields=['status', 'done_on', 'held'])
    elif action == 'note':
        item.note = request.POST.get('note', '').strip()[:300]
        item.save(update_fields=['note'])
    elif action == 'lessons':
        count = request.POST.get('lessons', '')
        item.lessons = max(1, min(MAX_LESSONS, int(count))) if count.isdigit() else item.lessons
        if item.status == 'todo' and item.held >= item.lessons:
            item.status, item.done_on = 'done', timezone.localdate()
        elif item.status == 'done' and item.held < item.lessons:
            item.status, item.done_on = 'todo', None
        item.save(update_fields=['lessons', 'status', 'done_on'])
    elif action == 'join':
        item.joined = request.POST.get('joined') == '1' and student.plan_items.filter(
            position__lt=item.position).exists()
        item.save(update_fields=['joined'])
    elif action == 'start_here':
        # Учень починає з цієї теми: попередні теми того самого курсу (класу дерева), що ще чекають, — пропущені
        earlier = student.plan_items.filter(position__lt=item.position, status='todo')
        if item.topic_id:
            earlier = earlier.filter(topic__chapter__grade_id=item.topic.chapter.grade_id)
        skipped = earlier.update(status='skipped')
        messages.success(request, f'▶ План починається з «{item.name}»; попередніх тем пропущено: {skipped}.')
    elif action == 'repeat':
        # Повторення — копія теми в кінці плану (її можна перемістити ближче)
        last = student.plan_items.aggregate(top=Max('position'))['top'] or 0
        copy = StudyPlanItem.objects.create(student=student, topic=item.topic, title=item.title, position=last + 1)
        messages.success(request, f'🔁 «{item.name}» додано в кінець плану ще раз — перемістіть, коли повторювати.')
        anchor = f'#item-{copy.id}'
    elif action == 'delete':
        with transaction.atomic():
            unjoin_next(student, item)
            item.delete()
            renumber(student)
        anchor = ''
    elif action in ('up', 'down', 'move'):
        with transaction.atomic():
            unjoin_next(student, item)
            item.joined = False
            item.save(update_fields=['joined'])
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
