"""Ціни шкільних уроків за правилами (SchoolPriceRule): перша тема кожного розділу — безкоштовна (якщо так
у правилі), решта уроків і узагальнення — за ціною теми, діагностика за клас — безкоштовна.
Матеріали НМТ, пакети й уроки з ручною ціною не змінюються."""
from .models import NMT_SUBJECT_NAME, CurriculumTopic, SchoolPriceRule, StudyMaterial


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
