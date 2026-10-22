"""Підписка учня на клас (ClassPlan / ClassSubscription): строки — як у підписки викладача (teachers.period_end),
доступ — через teachers.subscribed_grade_ids (усі опубліковані уроки й практика класу, поки підписка чинна)."""
import datetime

from django.core.cache import cache
from django.db.models import Count, Q, Sum
from django.utils import timezone

from .models import (NMT_SUBJECT_NAME, ClassPlan, ClassSubscription, CurriculumTopic, Order, StudyMaterial,
                     TutorStudentRequest)
from .teachers import period_end


def active_subscriptions(user):
    if not user.is_authenticated:
        return ClassSubscription.objects.none()
    return ClassSubscription.objects.filter(user=user, valid_until__gte=timezone.localdate())


def grant_class(user, plan, period, note=''):
    """Оплачено підписку на клас. Продовження того самого класу починається після кінця чинної підписки."""
    if period == 'support':
        return grant_support(user, plan, note=note)
    today = timezone.localdate()
    current = (active_subscriptions(user).filter(number=plan.number).order_by('-valid_until')
               .values_list('valid_until', flat=True).first())
    start = current + datetime.timedelta(days=1) if current else today
    return ClassSubscription.objects.create(user=user, number=plan.number, plan=plan,
                                            valid_until=period_end(start, period), note=note)


# Супровід: місяць підписки на клас, а учень на цей час — учень власника сайту (ДЗ з перевіркою, звіти батькам,
# сторінка для батьків). Місць обмежено (ClassPlan.support_seats в адмінці): час викладача не масштабується
def support_students():
    return TutorStudentRequest.objects.filter(status='approved', support_until__gte=timezone.localdate())


def support_seats_left(plan):
    taken = support_students().filter(course=f'grade_{plan.number}').count()
    return max(plan.support_seats - taken, 0)


def support_blocker(user):
    """Чому цьому користувачу не можна купити супровід, або '' (учень іншого репетитора — у нього свій викладач)"""
    request = getattr(user, 'tutor_request', None) if user.is_authenticated else None
    if request and request.status == 'approved' and request.teacher_id:
        return "Ви вже навчаєтеся з репетитором на платформі — супровід веде він."
    return ''


def grant_support(user, plan, note='', real_name=''):
    """Місяць супроводу: продовження — після кінця чинного супроводу (не річної підписки), і користувач стає
    учнем власника до цієї дати. Постійного учня (без дати супроводу) не чіпаємо — він і так учень."""
    today = timezone.localdate()
    current = (active_subscriptions(user).filter(number=plan.number, with_support=True).order_by('-valid_until')
               .values_list('valid_until', flat=True).first())
    start = current + datetime.timedelta(days=1) if current else today
    subscription = ClassSubscription.objects.create(user=user, number=plan.number, plan=plan, with_support=True,
                                                    valid_until=period_end(start, 'month'), note=note)
    request = TutorStudentRequest.objects.filter(user=user).first()
    if request is None:
        TutorStudentRequest.objects.create(
            user=user, real_name=real_name or user.get_full_name() or user.email, course=f'grade_{plan.number}',
            status='approved', support_until=subscription.valid_until)
    elif not (request.status == 'approved' and request.support_until is None):
        request.status, request.teacher = 'approved', None
        request.course = f'grade_{plan.number}'
        request.support_until = max(request.support_until or today, subscription.valid_until)
        if real_name:
            request.real_name = real_name
        request.save()
    return subscription


def end_expired_support():
    """Учні, у яких скінчився супровід, перестають бути учнями (історія лишається). Раз на день на процес"""
    today = timezone.localdate()
    if cache.add(f'support-expiry-{today}', True, 60 * 60 * 25):
        TutorStudentRequest.objects.filter(status='approved', support_until__lt=today).update(status='ended')


# Акція (оферта, п. 8.1; оголошена на сторінці «Підписка на клас»): сплачене за місячну підписку на клас протягом
# останніх UPGRADE_DAYS днів зараховується в ціну річної підписки на той самий клас
UPGRADE_DAYS = 30


def month_credit(user, plan):
    """Скільки гривень за місячні підписки на цей клас зарахувати в річну: оплати за останні UPGRADE_DAYS днів,
    зроблені після останньої річної підписки на цей клас (одну оплату не зараховуємо двічі)."""
    if not user.is_authenticated:
        return 0
    paid = Order.objects.filter(user=user, class_plan__number=plan.number, status='paid')
    last_year = paid.filter(plan_period='year').order_by('-paid_at').values_list('paid_at', flat=True).first()
    months = paid.filter(plan_period='month', paid_at__gte=timezone.now() - datetime.timedelta(days=UPGRADE_DAYS))
    if last_year:
        months = months.filter(paid_at__gt=last_year)
    return int(months.aggregate(total=Sum('total_amount'))['total'] or 0)


def price_for(user, plan, period):
    """Ціна для цього користувача: річна — мінус зараховані місячні оплати, але не менше за ціну місяця."""
    if period == 'month':
        return plan.price_month
    if period == 'support':
        return plan.support_price_month
    if not plan.price_year:
        return 0
    return max(plan.price_year - month_credit(user, plan), plan.price_month or 1)


def plans_on_sale():
    """Класи, що продаються, з наповненням: lessons_ready — опубліковані уроки з презентацією, lessons_total —
    теми-уроки класу за деревом, courses — назви курсів класу."""
    plans = [p for p in ClassPlan.objects.filter(is_active=True) if p.buy_options]
    if not plans:
        return []
    numbers = [p.number for p in plans]
    school = Q(chapter__grade__number__in=numbers) & ~Q(chapter__grade__subject__name=NMT_SUBJECT_NAME)
    totals = dict(CurriculumTopic.objects.filter(school, kind='lesson').values('chapter__grade__number')
                  .annotate(n=Count('id')).values_list('chapter__grade__number', 'n'))
    ready = dict(StudyMaterial.objects.filter(
        is_published=True, is_bundle=False, html_content__gt='', curriculum_topic__kind='lesson',
        curriculum_topic__chapter__grade__number__in=numbers)
        .exclude(curriculum_topic__chapter__grade__subject__name=NMT_SUBJECT_NAME)
        .values('curriculum_topic__chapter__grade__number').annotate(n=Count('id'))
        .values_list('curriculum_topic__chapter__grade__number', 'n'))
    courses = {}
    for number, subject in (CurriculumTopic.objects.filter(school).values_list(
            'chapter__grade__number', 'chapter__grade__subject__name').distinct()):
        courses.setdefault(number, set()).add(subject.split(' (')[0])
    for plan in plans:
        plan.lessons_total = totals.get(plan.number, 0)
        plan.lessons_ready = ready.get(plan.number, 0)
        names = sorted(courses.get(plan.number, ()), key=len)
        plan.courses = ' і '.join(names[:1] + [name.lower() for name in names[1:]])
    return plans


def plan_for_material(material):
    """Підписка, що продається й відкриває цей шкільний урок, або None."""
    grade = material.curriculum_grade
    if material.is_bundle or grade is None or grade.number is None or material.is_nmt:
        return None
    plan = ClassPlan.objects.filter(number=grade.number, is_active=True).first()
    return plan if plan and plan.buy_options else None


# Кошик: від стількох уроків одного класу підказуємо, що підписка на клас може бути вигіднішою
CART_HINT_MIN_LESSONS = 2


def cart_class_offers(user, items):
    """Підказки в кошику: [{plan, count, total, ready}] для класів, з яких у кошику щонайменше
    CART_HINT_MIN_LESSONS платних уроків, якщо клас продається помісячно, а підписки на нього в покупця немає.
    ready — скільки уроків класу вже відкриває підписка (без читання презентацій)."""
    by_number = {}
    for item in items:
        material = item.material
        if material.is_bundle or material.is_free or not material.price or material.is_nmt:
            continue
        number = material.curriculum_grade.number
        if number is not None:
            by_number.setdefault(number, []).append(material.price)
    by_number = {n: prices for n, prices in by_number.items() if len(prices) >= CART_HINT_MIN_LESSONS}
    if not by_number:
        return []
    subscribed = set(active_subscriptions(user).values_list('number', flat=True))
    plans = [p for p in ClassPlan.objects.filter(number__in=by_number, is_active=True, price_month__gt=0)
             if p.number not in subscribed]
    if not plans:
        return []
    ready = dict(StudyMaterial.objects.filter(
        is_published=True, is_bundle=False, html_content__gt='', curriculum_topic__kind='lesson',
        curriculum_topic__chapter__grade__number__in=[p.number for p in plans])
        .exclude(curriculum_topic__chapter__grade__subject__name=NMT_SUBJECT_NAME)
        .values('curriculum_topic__chapter__grade__number').annotate(n=Count('id'))
        .values_list('curriculum_topic__chapter__grade__number', 'n'))
    return [{'plan': plan, 'count': len(by_number[plan.number]), 'total': sum(by_number[plan.number]),
             'ready': ready.get(plan.number, 0)} for plan in plans]
