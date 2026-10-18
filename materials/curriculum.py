"""Спеціальні теми шкільних курсів: «Узагальнення: <розділ>» наприкінці кожного розділу і «Діагностика за <клас>»
на початку кожного класу. Кожна має свій (неопублікований, безкоштовний) урок — через нього працюють практика на уроці,
групи, ДЗ і звіти так само, як для звичайних тем. Урок узагальнення вчитель може опублікувати з презентацією.

Функція приймає класи моделей, щоб її можна було викликати і з міграції (історичні моделі), і з import_curriculum.
"""
NMT_SUBJECT_NAME = "Підготовка до НМТ / ЗНО"
SUMMARY_ORDER = 9999        # остання тема розділу
DIAGNOSTIC_CHAPTER = 'Діагностика'


def ensure_special_topics(Grade, Chapter, Topic, Material):
    created = 0
    for grade in Grade.objects.exclude(subject__name=NMT_SUBJECT_NAME).exclude(number__isnull=True):
        chapters = list(Chapter.objects.filter(grade=grade).exclude(name=DIAGNOSTIC_CHAPTER))
        if not chapters:
            continue
        for chapter in chapters:
            topic, made = Topic.objects.get_or_create(
                chapter=chapter, kind='summary',
                defaults={'name': f'Узагальнення: {chapter.name}', 'order': SUMMARY_ORDER})
            created += made
            Material.objects.get_or_create(curriculum_topic=topic, defaults={
                'title': topic.name, 'price': 0, 'is_free': True, 'is_published': False})
        chapter, _ = Chapter.objects.get_or_create(grade=grade, name=DIAGNOSTIC_CHAPTER, defaults={'order': 0})
        topic, made = Topic.objects.get_or_create(
            chapter=chapter, kind='diagnostic', defaults={'name': f'Діагностика за {grade.name}', 'order': 0})
        created += made
        Material.objects.get_or_create(curriculum_topic=topic, defaults={
            'title': f'{topic.name} ({grade.subject.name})', 'price': 0, 'is_free': True, 'is_published': False})
    return created
