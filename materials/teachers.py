"""Хто викладач і що йому видно.

* Власник сайту (is_staff / is_superuser) — усі матеріали; його учні — ті, в кого викладач не вказаний
  (заявки «Навчаєтесь у мене особисто?» і всі давніші) або вказаний він сам.
* Репетитор — користувач з активною підпискою (TeacherLicense) хоча б на один клас: показ уроків, практика,
  ДЗ і звіти лише в ліцензованих класах і лише для своїх учнів. Учень репетитора, поки в того є підписка,
  бачить усі уроки й практику свого класу (як учень власника) і практикується в усіх класах підписки
  без окремої оплати.

Чужих учнів, їхніх спроб, ДЗ і звітів викладач не бачить ніде.
"""
import calendar
import datetime
import secrets

from django.db.models import Q
from django.utils import timezone

from .models import (NMT_SUBJECT_NAME, ClassSubscription, CurriculumGrade, TeacherInvite, TeacherLicense,
                     TutorStudentRequest)

INVITE_ALPHABET = 'abcdefghjkmnpqrstuvwxyz23456789'   # без схожих символів (l/1, o/0)


def is_owner(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


def active_licenses(user):
    if not user.is_authenticated:
        return TeacherLicense.objects.none()
    return TeacherLicense.objects.filter(teacher=user, valid_until__gte=timezone.localdate())


def licensed_grade_ids(user):
    """None — усі класи (власник); інакше множина id класів з активної підписки: «Школа» — усі шкільні класи,
    «НМТ» — курс НМТ, «Один клас» — лише він."""
    if is_owner(user):
        return None
    grades = set()
    for scope, grade_id in active_licenses(user).values_list('scope', 'grade_id'):
        if scope == 'grade' and grade_id:
            grades.add(grade_id)
        elif scope == 'school':
            grades |= set(CurriculumGrade.objects.exclude(subject__name=NMT_SUBJECT_NAME)
                          .exclude(number__isnull=True).values_list('id', flat=True))
        elif scope == 'nmt':
            grades |= set(CurriculumGrade.objects.filter(subject__name=NMT_SUBJECT_NAME).values_list('id', flat=True))
    return grades


def is_tutor(user):
    """Чи має користувач кабінет викладача (урок з показом екрана, учні, ДЗ, звіти)."""
    return is_owner(user) or bool(licensed_grade_ids(user))


def can_teach(user, material):
    """Чи може викладач показувати цей урок і вести з нього практику."""
    grades = licensed_grade_ids(user)
    if grades is None:
        return is_owner(user)
    grade = material.curriculum_grade
    return grade is not None and grade.id in grades


def students_of(user):
    """Підтверджені учні викладача."""
    if not user.is_authenticated:
        return TutorStudentRequest.objects.none()
    mine = Q(teacher=user)
    if is_owner(user):
        mine |= Q(teacher__isnull=True)
    return TutorStudentRequest.objects.filter(mine, status='approved')


def teaches(user, pupil_user):
    """Чи є pupil_user учнем цього викладача."""
    return students_of(user).filter(user=pupil_user).exists()


def covered_by_teacher(pupil, material):
    """Учень репетитора практикується в класах, на які в його викладача є підписка."""
    if not pupil.is_authenticated:
        return False
    request = TutorStudentRequest.objects.filter(user=pupil, status='approved', teacher__isnull=False).first()
    grade = material.curriculum_grade
    return bool(request and grade and grade.id in (licensed_grade_ids(request.teacher) or set()))


def taught_class_grade_ids(user):
    """Учень (заявку «N клас» підтверджено) бачить усі уроки й практику свого класу в кожному шкільному курсі
    (5–6 — математика, 7–11 — алгебра й геометрія), поки навчається, зокрема ще не опубліковані: учень власника
    сайту — завжди, учень репетитора — у тих курсах свого класу, які покриває чинна підписка репетитора.
    Повертає множину id класів; результат кешується на об'єкті користувача на час запиту."""
    if not user.is_authenticated:
        return set()
    if not hasattr(user, '_taught_class_grade_ids'):
        grades = set()
        request = TutorStudentRequest.objects.filter(user=user, status='approved', course__startswith='grade_') \
            .select_related('teacher').first()
        if request:
            number = int(request.course.split('_')[1])
            grades = set(CurriculumGrade.objects.filter(number=number).exclude(subject__name=NMT_SUBJECT_NAME)
                         .values_list('id', flat=True))
            licensed = licensed_grade_ids(request.teacher) if request.teacher is not None else None
            if licensed is not None:
                grades &= licensed
        user._taught_class_grade_ids = grades
    return user._taught_class_grade_ids


def subscribed_grade_ids(user):
    """Класи з чинною підпискою учня на клас (materials/subscriptions.py): усі опубліковані уроки й практика."""
    if not user.is_authenticated:
        return set()
    if not hasattr(user, '_subscribed_grade_ids'):
        numbers = set(ClassSubscription.objects.filter(user=user, valid_until__gte=timezone.localdate())
                      .values_list('number', flat=True))
        user._subscribed_grade_ids = set(
            CurriculumGrade.objects.filter(number__in=numbers).exclude(subject__name=NMT_SUBJECT_NAME)
            .values_list('id', flat=True)) if numbers else set()
    return user._subscribed_grade_ids


def in_own_class(user, material):
    """Чи відкрита тема учневі без купівлі: свій клас — будь-яка, клас із підпискою — лише опублікована."""
    if material.is_bundle:
        return False
    grade = material.curriculum_grade
    if grade is None:
        return False
    return grade.id in taught_class_grade_ids(user) or (material.is_published and grade.id in subscribed_grade_ids(user))


def invite_for(user):
    invite = TeacherInvite.objects.filter(teacher=user).first()
    if invite is None:
        code = ''.join(secrets.choice(INVITE_ALPHABET) for _ in range(8))
        invite = TeacherInvite.objects.create(teacher=user, code=code)
    return invite


# ---------- Ліміт учнів, пробний період, продовження ----------

TRIAL_DAYS = 14
TRIAL_STUDENTS = 2


def student_limit(user):
    """Скільки учнів може мати викладач: None — без обмежень (власник або тариф без ліміту)."""
    if is_owner(user):
        return None
    # Ліміт задає шкільна підписка; додаток НМТ своїх учнів не додає (крім випадку, коли є лише він)
    licenses = active_licenses(user)
    base = licenses.exclude(scope='nmt') if licenses.exclude(scope='nmt').exists() else licenses
    limits = list(base.values_list('max_students', flat=True))
    if not limits or None in limits:
        return None
    return max(limits)


def student_count(user):
    return TutorStudentRequest.objects.filter(teacher=user, status='approved').count()


def can_accept_student(user):
    limit = student_limit(user)
    return limit is None or student_count(user) < limit


def trial_available(user):
    """Пробний період — один раз, лише тому, хто ще ніколи не мав підписки."""
    return user.is_authenticated and not is_owner(user) and not TeacherLicense.objects.filter(teacher=user).exists()


def start_trial(user):
    until = timezone.localdate() + datetime.timedelta(days=TRIAL_DAYS)
    for scope in ('school', 'nmt'):
        TeacherLicense.objects.create(teacher=user, scope=scope, valid_until=until, max_students=TRIAL_STUDENTS,
                                      is_trial=True, note='Пробний період')
    return until


def add_months(day, months):
    month = day.month - 1 + months
    year, month = day.year + month // 12, month % 12 + 1
    return datetime.date(year, month, min(day.day, calendar.monthrange(year, month)[1]))


def period_end(start, period):
    """Місяць — до того самого числа наступного місяця. Навчальний рік — до 30 червня; якщо до нього лишилося
    менше трьох місяців, — до 30 червня наступного року (покупка навесні покриває й наступний рік)."""
    if period == 'month':
        return add_months(start, 1)
    end = datetime.date(start.year if start.month <= 6 else start.year + 1, 6, 30)
    if (end - start).days < 92:
        end = datetime.date(end.year + 1, 6, 30)
    return end


def grant_plan(user, plan, period, note=''):
    """Оплачено тариф. Продовження того самого тарифу починається після кінця чинного (дні, що лишилися,
    не пропадають); інший тариф (наприклад, перехід зі «Старту» на «Профі») діє одразу."""
    today = timezone.localdate()
    current = (TeacherLicense.objects.filter(teacher=user, plan=plan, is_trial=False, valid_until__gte=today)
               .order_by('-valid_until').values_list('valid_until', flat=True).first())
    start = current + datetime.timedelta(days=1) if current else today
    return TeacherLicense.objects.create(
        teacher=user, scope=plan.kind, plan=plan, valid_until=period_end(start, period),
        max_students=plan.max_students if plan.kind == 'school' else None, note=note)

