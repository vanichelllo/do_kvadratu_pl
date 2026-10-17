"""Курс «Підготовка до НМТ» у класифікаторі не збігався з 46 конспектами: тем 21–23 не було, а теми 4, 9,
12–14, 17, 18 мали інші назви. Конспекти й завдання прив'язуються до тем за номером, тож частина потрапила
на чужі теми, а 21–23 лишилися без теми. Міграція приводить курс до списку конспектів і переприв'язує дані."""
import ast
import re
from pathlib import Path

from django.conf import settings
from django.db import migrations

NMT_SUBJECT_NAME = "Підготовка до НМТ / ЗНО"
NMT_GRADE_NAME = "Підготовка до НМТ"
NUMBER = re.compile(r'^(\d+)\.\s')

# (назва розділу, порядок розділу, [(номер, назва теми)]); розділи алгебри мають порядок <= 540 (діагностика ділить так)
NMT_CHAPTERS = [
    ("Розділ 1. Числа і вирази", 480, [
        (1, "Числові множини"), (2, "Відношення, пропорції та відсотки"), (3, "Степені"),
        (4, "Одночлени, многочлени та формули скороченого множення"),
        (5, "Розкладання на множники. Дробово-раціональні вирази")]),
    ("Розділ 2. Рівняння і корені", 490, [
        (6, "Лінійні рівняння. Лінійні рівняння з модулем"), (7, "Квадратні рівняння"),
        (8, "Дробово-раціональні рівняння"), (9, "Корені та їх властивості"), (10, "Ірраціональні рівняння")]),
    ("Розділ 3. Функції, нерівності та системи", 500, [
        (11, "Функції та їх властивості"), (12, "Квадратична функція"), (13, "Лінійні нерівності"),
        (14, "Квадратичні нерівності. Дробово-раціональні нерівності"), (15, "Системи рівнянь"),
        (16, "Системи нерівностей")]),
    ("Розділ 4. Тригонометрія", 510, [
        (17, "Тригонометричні вирази"), (18, "Тригонометричні рівняння")]),
    ("Розділ 5. Показникові та логарифмічні вирази, рівняння і нерівності", 520, [
        (19, "Показникові вирази"), (20, "Логарифмічні вирази"), (21, "Показникові рівняння"),
        (22, "Логарифмічні рівняння"), (23, "Показникові та логарифмічні нерівності")]),
    ("Розділ 6. Графіки, послідовності, похідна та інтеграл", 530, [
        (24, "Побудова графіків функцій шляхом геометричних перетворень"), (25, "Числові послідовності"),
        (26, "Похідна"), (27, "Первісна та інтеграл")]),
    ("Розділ 7. Комбінаторика, ймовірність і статистика", 540, [
        (28, "Комбінаторика"), (29, "Початки теорії ймовірностей та елементи статистики")]),
    ("Розділ 8. Планіметрія", 550, [
        (30, "Найпростіші геометричні фігури"), (31, "Трикутники"), (32, "Рівнобедрений трикутник"),
        (33, "Прямокутний трикутник"), (34, "Теорема косинусів та теорема синусів"), (35, "Площа трикутника"),
        (36, "Чотирикутники"), (37, "Многокутники"), (38, "Коло та круг")]),
    ("Розділ 9. Стереометрія", 560, [
        (39, "Вступ до стереометрії"), (40, "Призма"), (41, "Піраміда"), (42, "Циліндр"), (43, "Конус"),
        (44, "Сфера та куля")]),
    ("Розділ 10. Координати та вектори", 570, [
        (45, "Координати на площині та у просторі"), (46, "Вектори на площині та у просторі")]),
]


def _normalize(text):
    return ' '.join(str(text).split()).lower()


def _bank_tasks(base_dir):
    """(номер теми, текст завдання) з файлів import_files/bank_*.py — без виконання файлів."""
    for path in sorted(Path(base_dir, 'import_files').glob('bank_*.py')):
        try:
            values = {}
            for node in ast.parse(path.read_text(encoding='utf-8')).body:
                if (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                        and node.targets[0].id in ('TOPIC_NAME', 'TASKS')):
                    values[node.targets[0].id] = ast.literal_eval(node.value)
        except (OSError, SyntaxError, ValueError):
            continue
        match = NUMBER.match(str(values.get('TOPIC_NAME', '')))
        if not match or not isinstance(values.get('TASKS'), list):
            continue
        for task in values['TASKS']:
            if isinstance(task, dict) and task.get('text'):
                yield int(match.group(1)), task['text']


def forwards(apps, schema_editor):
    CurriculumGrade = apps.get_model('materials', 'CurriculumGrade')
    CurriculumChapter = apps.get_model('materials', 'CurriculumChapter')
    CurriculumTopic = apps.get_model('materials', 'CurriculumTopic')
    StudyMaterial = apps.get_model('materials', 'StudyMaterial')
    Question = apps.get_model('materials', 'Question')

    grade = CurriculumGrade.objects.filter(subject__name=NMT_SUBJECT_NAME, name=NMT_GRADE_NAME).first()
    if grade is None:
        return  # класифікатор ще не завантажено — import_curriculum створить курс уже правильним

    # 1. Наявні теми НМТ перейменовуємо за номером (зв'язки з конспектами й завданнями зберігаються), бракуючі створюємо
    existing = {}
    for topic in CurriculumTopic.objects.filter(chapter__grade=grade).order_by('id'):
        match = NUMBER.match(topic.name)
        if match:
            existing.setdefault(int(match.group(1)), topic)
    topics, titles, created = {}, {}, set()
    for chapter_name, chapter_order, items in NMT_CHAPTERS:
        chapter, _ = CurriculumChapter.objects.get_or_create(grade=grade, name=chapter_name,
                                                             defaults={'order': chapter_order})
        if chapter.order != chapter_order:
            chapter.order = chapter_order
            chapter.save(update_fields=['order'])
        for number, title in items:
            topic = existing.get(number)
            if topic is None:
                topic, _ = CurriculumTopic(chapter=chapter), created.add(number)
            topic.chapter, topic.name, topic.order = chapter, f"{number}. {title}", 5000 + number
            topic.save()
            topics[number], titles[number] = topic, _normalize(topic.name)
    CurriculumChapter.objects.filter(grade=grade, topics__isnull=True).delete()

    # 2. Конспекти НМТ («N. Назва») — на тему з тим самим номером. Конспект з іншого курсу переносимо, лише якщо
    #    його назва точно збігається з темою НМТ (так 21–23, вручну прив'язані до 11 класу, повертаються в НМТ)
    for material in StudyMaterial.objects.filter(is_bundle=False).select_related('curriculum_topic__chapter'):
        match = NUMBER.match(material.title)
        number = int(match.group(1)) if match else None
        if number not in topics:
            continue
        current = material.curriculum_topic
        in_nmt = current is None or current.chapter.grade_id == grade.id
        if (in_nmt or _normalize(material.title) == titles[number]) and material.curriculum_topic_id != topics[number].id:
            material.curriculum_topic = topics[number]
            material.save(update_fields=['curriculum_topic'])

    # 3. Завдання без теми (з банків 21–23 їх не було куди прив'язати) — за текстом з файлів банку.
    #    Однаковий текст буває в кількох банках: тоді беремо тему, якої раніше не було (саме її завдання лишилися
    #    без теми), а якщо однозначно визначити не вдається — не чіпаємо
    banks_by_text = {}
    for number, text in _bank_tasks(settings.BASE_DIR):
        if number in topics:
            banks_by_text.setdefault(_normalize(text), set()).add(number)
    for pk, text in Question.objects.filter(curriculum_topic__isnull=True).values_list('id', 'text'):
        numbers = banks_by_text.get(_normalize(text), set())
        candidates = (numbers & created) or numbers
        if len(candidates) == 1:
            Question.objects.filter(id=pk).update(curriculum_topic=topics[candidates.pop()])


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0032_studymaterial_neutral_default_description'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
