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


# ---------- Доповнення дерева тем (жовтень 2026) ----------
# Теми, яких бракувало порівняно з підручниками. Наявні теми переназиваються (а не створюються заново), щоб
# прив'язані до них уроки, завдання й результати лишилися на місці. Формат розділу:
# (курс, клас, назва розділу, нова назва розділу або None, [(назва теми, порядок, стара назва або None), ...]).
TREE_UPDATE_2026_10 = [
    ("Алгебра (7-9 класи)", "7 клас", "Розділ 2. Цілі вирази. Одночлени та многочлени", None, [
        ("2.7. Розкладання многочлена на множники. Винесення спільного множника за дужки", 1107, None),
        ("2.8. Розкладання многочлена на множники. Спосіб групування", 1108, None),
    ]),
    ("Алгебра (7-9 класи)", "8 клас", "Розділ 1. Раціональні вирази", None, [
        ("1.8. Функція y = k/x та її графік", 1508, None),
    ]),
    ("Алгебра (7-9 класи)", "9 клас", "Розділ 4. Основи комбінаторики, теорії ймовірностей та статистики",
     "Розділ 4. Елементи прикладної математики", [
        ("4.1. Математичне моделювання", 2101, None),
        ("4.2. Відсоткові розрахунки", 2102, None),
        ("4.3. Абсолютна і відносна похибки. Наближені обчислення", 2103, None),
        ("4.4. Комбінаторні правила суми та добутку", 2104, "4.1. Комбінаторні правила суми та добутку"),
        ("4.5. Ймовірність випадкової події", 2105, "4.2. Ймовірність випадкової події"),
        ("4.6. Початкові відомості про статистику", 2106, "4.3. Початкові відомості про статистику"),
    ]),
    ("Алгебра і початки аналізу (10-11 класи)", "10 клас", "Розділ 3. Тригонометричні рівняння і нерівності", None, [
        ("3.4. Тригонометричні нерівності", 3704, None),
    ]),
    ("Геометрія (7-9 класи)", "7 клас", "Розділ 4. Коло і круг. Геометричні побудови", None, [
        ("4.1. Геометричне місце точок. Коло, круг та їх елементи", 2501, "4.1. Коло, круг та їх елементи"),
        ("4.4. Задачі на побудову", 2504, None),
        ("4.5. Метод геометричних місць точок у задачах на побудову", 2505, None),
    ]),
    ("Геометрія (7-9 класи)", "8 клас", "Розділ 1. Чотирикутники", None, [
        ("1.4. Середня лінія трикутника", 2604, None),
        ("1.5. Трапеція. Середня лінія трапеції", 2605, "1.4. Трапеція. Середня лінія трапеції"),
        ("1.6. Центральні та вписані кути", 2606, None),
        ("1.7. Вписані та описані чотирикутники", 2607, "1.5. Вписані та описані чотирикутники"),
    ]),
]


def apply_tree_update(Grade, Chapter, Topic, Material, update=TREE_UPDATE_2026_10):
    """Застосовує доповнення до вже завантаженого класифікатора; повторний запуск нічого не змінює.
    Класу чи розділу немає (класифікатор не завантажено) — пропускаємо: import_curriculum створить усе одразу правильно.
    Урок, назва якого збігалася зі старою назвою теми чи узагальнення, переназивається разом із нею."""
    changed = 0
    for subject, grade_name, chapter_name, new_chapter_name, topics in update:
        grade = Grade.objects.filter(subject__name=subject, name=grade_name).first()
        if grade is None:
            continue
        chapter = (Chapter.objects.filter(grade=grade, name=chapter_name).first()
                   or (new_chapter_name and Chapter.objects.filter(grade=grade, name=new_chapter_name).first()))
        if chapter is None:
            continue
        if new_chapter_name and chapter.name != new_chapter_name:
            chapter.name = new_chapter_name
            chapter.save(update_fields=['name'])
            summary = Topic.objects.filter(chapter=chapter, kind='summary').first()
            if summary is not None:
                old_summary, summary.name = summary.name, f'Узагальнення: {new_chapter_name}'
                summary.save(update_fields=['name'])
                Material.objects.filter(curriculum_topic=summary, title=old_summary).update(title=summary.name)
            changed += 1
        for name, order, old_name in topics:
            topic = (old_name and Topic.objects.filter(chapter=chapter, name=old_name).first()) \
                or Topic.objects.filter(chapter=chapter, name=name).first()
            if topic is None:
                Topic.objects.create(chapter=chapter, name=name, order=order, kind='lesson')
                changed += 1
            elif (topic.name, topic.order) != (name, order):
                old = topic.name
                topic.name, topic.order = name, order
                topic.save(update_fields=['name', 'order'])
                Material.objects.filter(curriculum_topic=topic, title=old).update(title=name)
                changed += 1
    return changed
