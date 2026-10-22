"""Ціни шкільних уроків за правилами (SchoolPriceRule): перша тема кожного розділу — безкоштовна (якщо так
у правилі), решта уроків і узагальнення — за ціною теми, діагностика за клас — безкоштовна.
Матеріали НМТ, пакети й уроки з ручною ціною не змінюються.

Пакети розділів (sync_chapter_bundles): усі уроки розділу за BUNDLE_SHARE суми платних тем, але не дорожче за
BUNDLE_CAP_MONTHS місячних підписок на клас."""
from django.contrib.auth import get_user_model

from .models import NMT_SUBJECT_NAME, ClassPlan, CurriculumChapter, CurriculumTopic, SchoolPriceRule, StudyMaterial

BUNDLE_SHARE = 0.7
BUNDLE_CAP_MONTHS = 1.5
BUNDLE_MIN_PAID = 2   # пакет має сенс, коли в розділі щонайменше 2 платні уроки


def school_materials():
    return (StudyMaterial.objects.filter(is_bundle=False, price_is_manual=False, curriculum_topic__isnull=False)
            .exclude(curriculum_topic__chapter__grade__subject__name=NMT_SUBJECT_NAME)
            .select_related('curriculum_topic__chapter'))


def first_topic_ids(chapter_ids):
    """Перша тема-урок кожного розділу."""
    first = {}
    for topic_id, chapter_id in (CurriculumTopic.objects.filter(chapter_id__in=chapter_ids, kind='lesson')
                                 .order_by('chapter_id', 'order', 'id').values_list('id', 'chapter_id')):
        first.setdefault(chapter_id, topic_id)
    return set(first.values())


def rule_price(material, rule, first_ids):
    """(price, is_free) за правилом."""
    topic = material.curriculum_topic
    if topic.kind == 'diagnostic' or (rule.first_topic_free and topic.id in first_ids):
        return 0, True
    return rule.topic_price, False


def apply_price_rules(materials=None):
    """Ставить ціни за правилами; повертає кількість змінених матеріалів. Без жодного правила нічого не робить."""
    rules = {rule.grade_id: rule for rule in SchoolPriceRule.objects.all()}
    if not rules:
        return 0
    materials = list(school_materials() if materials is None else materials)
    first_ids = first_topic_ids({m.curriculum_topic.chapter_id for m in materials})
    changed = []
    for material in materials:
        rule = rules.get(material.curriculum_topic.chapter.grade_id) or rules.get(None)
        if rule is None:
            continue
        price, is_free = rule_price(material, rule, first_ids)
        if (material.price, material.is_free) != (price, is_free):
            material.price, material.is_free = price, is_free
            changed.append(material)
    StudyMaterial.objects.bulk_update(changed, ['price', 'is_free'])
    return len(changed)


def bundle_price(paid_sum, month_price):
    """Ціна пакета розділу: BUNDLE_SHARE суми платних тем, не більше BUNDLE_CAP_MONTHS місячних підписок."""
    price = int(paid_sum * BUNDLE_SHARE + 0.5)
    if month_price:
        price = min(price, int(month_price * BUNDLE_CAP_MONTHS + 0.5))
    return price


def sync_chapter_bundles():
    """Пакет для кожного шкільного розділу з BUNDLE_MIN_PAID+ опублікованими платними уроками: склад — усі
    опубліковані уроки розділу, ціна — за bundle_price (ручну ціну з адмінки не чіпаємо). Нові уроки пакета
    відкриваються тим, хто його вже купив. Знятий з публікації пакет назад не публікується.
    Повертає (створено, оновлено)."""
    lessons = (StudyMaterial.objects.filter(is_published=True, is_bundle=False, curriculum_topic__isnull=False)
               .exclude(curriculum_topic__chapter__grade__subject__name=NMT_SUBJECT_NAME)
               .values_list('id', 'price', 'is_free', 'curriculum_topic__chapter_id'))
    by_chapter = {}
    for material_id, price, is_free, chapter_id in lessons:
        by_chapter.setdefault(chapter_id, []).append((material_id, 0 if is_free else price))
    months = dict(ClassPlan.objects.filter(price_month__gt=0).values_list('number', 'price_month'))
    bundles = {b.bundle_chapter_id: b for b in StudyMaterial.objects.filter(bundle_chapter__isnull=False)}
    created = updated = 0
    for chapter in CurriculumChapter.objects.filter(id__in=by_chapter).select_related('grade__subject'):
        items = by_chapter[chapter.id]
        paid = [price for _, price in items if price]
        bundle = bundles.get(chapter.id)
        if len(paid) < BUNDLE_MIN_PAID and bundle is None:
            continue
        price = bundle_price(sum(paid), months.get(chapter.grade.number))
        if bundle is None:
            bundle = StudyMaterial.objects.create(
                title=f"Пакет: {chapter.name} · {chapter.grade.short_label}", is_bundle=True,
                bundle_chapter=chapter, price=price, is_published=True,
                description="Усі уроки розділу з практикою за ціною нижчою, ніж поодинці. Нові уроки розділу "
                            "з'являються в пакеті й відкриваються покупцям автоматично.")
            created += 1
        elif not bundle.price_is_manual and bundle.price != price:
            bundle.price = price
            bundle.save(update_fields=['price'])
            updated += 1
        included = set(bundle.included_materials.values_list('id', flat=True))
        new_ids = {material_id for material_id, _ in items} - included
        if new_ids:
            bundle.included_materials.add(*new_ids)
            for buyer in get_user_model().objects.filter(orders__status='paid',
                                                         orders__items__material=bundle).distinct():
                buyer.purchased_materials.add(*new_ids)
    return created, updated
