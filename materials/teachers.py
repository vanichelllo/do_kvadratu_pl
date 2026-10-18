"""Хто викладач і що йому видно.

* Власник сайту (is_staff / is_superuser) — усі матеріали; його учні — ті, в кого викладач не вказаний
  (заявки «Навчаєтесь у мене особисто?» і всі давніші) або вказаний він сам.
* Репетитор — користувач з активною підпискою (TeacherLicense) хоча б на один клас: показ уроків, практика,
  ДЗ і звіти лише в ліцензованих класах і лише для своїх учнів. Учні репетитора практикуються в цих класах
  без окремої оплати.

Чужих учнів, їхніх спроб, ДЗ і звітів викладач не бачить ніде.
"""
import secrets

from django.db.models import Q
from django.utils import timezone

from .models import TeacherInvite, TeacherLicense, TutorStudentRequest

INVITE_ALPHABET = 'abcdefghjkmnpqrstuvwxyz23456789'   # без схожих символів (l/1, o/0)


def is_owner(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


def active_licenses(user):
    if not user.is_authenticated:
        return TeacherLicense.objects.none()
    return TeacherLicense.objects.filter(teacher=user, valid_until__gte=timezone.localdate())


def licensed_grade_ids(user):
    """None — усі класи (власник); інакше множина id класів з активною підпискою."""
    if is_owner(user):
        return None
    return set(active_licenses(user).values_list('grade_id', flat=True))


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
    return bool(request and grade and active_licenses(request.teacher).filter(grade=grade).exists())


def invite_for(user):
    invite = TeacherInvite.objects.filter(teacher=user).first()
    if invite is None:
        code = ''.join(secrets.choice(INVITE_ALPHABET) for _ in range(8))
        invite = TeacherInvite.objects.create(teacher=user, code=code)
    return invite
