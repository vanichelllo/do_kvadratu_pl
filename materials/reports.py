"""Звіт продажів для власника (адмінка → «Замовлення» → «📊 Звіт продажів»): помісячні продажі за видами товарів,
надходження карткою, повернення; чинні підписки учнів і викладачів; теми, які найбільше практикують."""
import datetime
from decimal import Decimal

from django.db.models import Count
from django.utils import timezone

from .models import NMT_SUBJECT_NAME, ClassSubscription, Order, PracticeAttempt, TeacherLicense

MONTHS_UA = ['січень', 'лютий', 'березень', 'квітень', 'травень', 'червень', 'липень', 'серпень', 'вересень',
             'жовтень', 'листопад', 'грудень']
BALANCE = 'balance_payment'


def month_bounds(count):
    """[(назва, початок, кінець)] — останні count місяців, від поточного назад; межі — за київським часом."""
    today = timezone.localdate()
    year, month = today.year, today.month
    bounds = []
    for _ in range(count):
        start = datetime.date(year, month, 1)
        end = datetime.date(year + (month == 12), month % 12 + 1, 1)
        aware = lambda d: timezone.make_aware(datetime.datetime.combine(d, datetime.time.min))
        bounds.append((f'{MONTHS_UA[month - 1]} {year}', aware(start), aware(end)))
        year, month = (year - 1, 12) if month == 1 else (year, month - 1)
    return bounds


def material_split(order):
    """Сума замовлення матеріалів, поділена на НМТ і шкільні уроки пропорційно до цін позицій (знижки враховано)."""
    items = list(order.items.all())
    base = sum((item.price for item in items), Decimal(0))
    school = sum((item.price for item in items if item.material and not item.material.is_nmt), Decimal(0))
    total = Decimal(order.total_amount)
    school_part = (total * school / base).quantize(Decimal(1)) if base else Decimal(0)
    return total - school_part, school_part


def month_row(label, start, end):
    paid = (Order.objects.filter(status='paid', paid_at__gte=start, paid_at__lt=end)
            .prefetch_related('items__material__curriculum_topic__chapter__grade__subject'))
    row = {'label': label, 'nmt': Decimal(0), 'school': Decimal(0), 'nmt_n': 0, 'school_n': 0,
           'class_new': 0, 'class_renew': 0, 'class_sum': Decimal(0), 'tutor_n': 0, 'tutor_sum': Decimal(0),
           'topup': Decimal(0), 'card': Decimal(0)}
    for order in paid:
        amount = Decimal(order.total_amount)
        if order.mono_invoice_id != BALANCE:
            row['card'] += amount
        if order.class_plan_id:
            renewal = Order.objects.filter(user=order.user_id, class_plan__number=order.class_plan.number,
                                           status='paid', paid_at__lt=order.paid_at).exists()
            row['class_renew' if renewal else 'class_new'] += 1
            row['class_sum'] += amount
        elif order.teacher_plan_id:
            row['tutor_n'] += 1
            row['tutor_sum'] += amount
        elif order.items.all():
            nmt, school = material_split(order)
            row['nmt'] += nmt
            row['school'] += school
            row['nmt_n'] += int(bool(nmt))
            row['school_n'] += int(bool(school))
        elif order.mono_invoice_id != BALANCE:
            row['topup'] += amount
    refunds = Order.objects.filter(status='refunded', created_at__gte=start, created_at__lt=end)
    row['refund_n'] = refunds.count()
    row['refund_sum'] = sum((Decimal(o.total_amount) for o in refunds), Decimal(0))
    row['sold'] = row['nmt'] + row['school'] + row['class_sum'] + row['tutor_sum']
    return row


def sales_report(months=6):
    today = timezone.localdate()
    subs = (ClassSubscription.objects.filter(valid_until__gte=today).values('number')
            .annotate(users=Count('user', distinct=True)).order_by('number'))
    licenses = (TeacherLicense.objects.filter(valid_until__gte=today, is_trial=False).values('plan__name')
                .annotate(teachers=Count('teacher', distinct=True)).order_by('plan__name'))
    since = timezone.now() - datetime.timedelta(days=30)
    practice = (PracticeAttempt.objects.filter(created_at__gte=since, material__curriculum_topic__isnull=False)
                .exclude(material__curriculum_topic__chapter__grade__subject__name=NMT_SUBJECT_NAME)
                .values('material__title', 'material__curriculum_topic__chapter__grade__name')
                .annotate(n=Count('id'), users=Count('user', distinct=True)).order_by('-n')[:10])
    return {
        'rows': [month_row(*bounds) for bounds in month_bounds(months)],
        'class_subscriptions': list(subs),
        'tutor_licenses': list(licenses),
        'trials': TeacherLicense.objects.filter(valid_until__gte=today, is_trial=True)
                                        .values('teacher').distinct().count(),
        'top_practice': list(practice),
    }
