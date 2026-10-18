"""Домашні завдання: вчитель задає практику з теми до дати, учень проходить її вдома на своєму акаунті.

Результат ДЗ — перша спроба учня після видачі: вона й чесна, і порівнянна з уроком. Статус рахується
з того, що є в базі: спроба, незавершена практика (почав і кинув) або нічого.
"""
from django.utils import timezone

from .models import Homework, PracticeAttempt, PracticeRun
from .practice import overall_grade

LABELS = {
    'done': '🟢 Виконано',
    'late': '🟡 Виконано із запізненням',
    'started': '🟠 Почав, не завершив',
    'waiting': '⚪ Задано',
    'overdue': '🔴 Не виконано',
}
# Статус ДЗ для звіту заняття (StudentReport.HW_CHOICES)
REPORT_STATUS = {'done': 'completed', 'late': 'completed', 'started': 'partial', 'overdue': 'not_submitted'}
# На скільки балів оцінка вдома має перевищувати урочну, щоб попередити вчителя
GAP_WARNING = 4


def grants_access(user, material):
    """Задане ДЗ відкриває практику з теми, навіть якщо учень її не купував."""
    return user.is_authenticated and Homework.objects.filter(student__user=user, material=material).exists()


def link_attempt(attempt):
    """Перша спроба учня після видачі стає результатом усіх відкритих ДЗ з цієї теми."""
    Homework.objects.filter(student__user=attempt.user, material=attempt.material, attempt__isnull=True,
                            created_at__lte=attempt.created_at).update(attempt=attempt)


def annotate(homeworks):
    """Додає кожному ДЗ state, label, answered (скільки завдань розв'язано в незавершеній практиці) і warning."""
    homeworks = list(homeworks)
    if not homeworks:
        return homeworks
    user_ids = {hw.student.user_id for hw in homeworks}
    material_ids = {hw.material_id for hw in homeworks}
    runs = {}
    for run in PracticeRun.objects.filter(user_id__in=user_ids, material_id__in=material_ids, teacher__isnull=True,
                                          finished_at__isnull=True):
        runs.setdefault((run.user_id, run.material_id), []).append(run)
    lessons = {}
    for attempt in (PracticeAttempt.objects.filter(user_id__in=user_ids, material_id__in=material_ids,
                                                   conducted_by__isnull=False).order_by('created_at')):
        lessons[(attempt.user_id, attempt.material_id)] = attempt   # остання урочна спроба
    today = timezone.localdate()
    for hw in homeworks:
        key = (hw.student.user_id, hw.material_id)
        hw.answered = 0
        hw.warning = ''
        if hw.attempt_id:
            hw.state = 'late' if timezone.localtime(hw.attempt.created_at).date() > hw.due_date else 'done'
            lesson = lessons.get(key)
            home_grade, lesson_grade = overall_grade(hw.attempt), overall_grade(lesson) if lesson else None
            if home_grade and lesson_grade and home_grade - lesson_grade >= GAP_WARNING:
                hw.warning = (f'Вдома {home_grade}, на уроці {lesson_grade} — варто перевірити, '
                              f'чи учень розв\'язував сам.')
        else:
            started = [r for r in runs.get(key, []) if r.created_at >= hw.created_at]
            hw.answered = max((sum(1 for e in r.state.get('history', []) if e.get('tries')) for r in started),
                              default=0)
            hw.state = 'started' if hw.answered else ('overdue' if today > hw.due_date else 'waiting')
        hw.label = LABELS[hw.state]
    return homeworks


def report_status(student):
    """Статус ДЗ для звіту заняття — з останнього заданого ДЗ; None, якщо ще не час судити."""
    latest = Homework.objects.filter(student=student).select_related('student', 'attempt').first()
    if latest is None:
        return 'not_assigned'
    return REPORT_STATUS.get(annotate([latest])[0].state)
