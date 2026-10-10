"""Завантаження банку завдань з файлу формату import_files/bank_*.py (сторінка в адмінці).

Файл НЕ виконується: його вміст читається через ast.literal_eval, тож у ньому можливі лише
літерали (рядки, числа, списки, кортежі, словники). Спершу будується пробний звіт без запису
в базу, потім той самий файл можна імпортувати (логіка імпорту — як у run_import.py).
"""
import ast
from dataclasses import dataclass, field

from django.db import transaction

from .models import AnswerOption, DiagnosticTopic, MatchItem, Question, StudyMaterial

MAX_FILE_BYTES = 2 * 1024 * 1024

# Теги з відомими помилками в назві → правильна назва конспекту
TAG_ALIASES = {
    '34. Теореми косинусів та теорема синусів': '34. Теорема косинусів та теорема синусів',
}

TYPES = ('CHOICE', 'MATCH', 'SHORT')
SHORT_ANSWER_MAX = 50  # Question.correct_short_answer
OPTION_TEXT_MAX = 255  # AnswerOption.text, MatchItem.text


class BankFormatError(Exception):
    """Файл не вдалося прочитати як банк завдань (повідомлення зрозуміле користувачу)."""


@dataclass
class ImportReport:
    topic_name: str = ''
    total: int = 0
    to_add: list = field(default_factory=list)       # індекси завдань, які буде додано
    duplicates: list = field(default_factory=list)   # (індекс, текст) — вже є в базі або повтор у файлі
    errors: list = field(default_factory=list)       # (індекс, текст помилки)
    unknown_tags: dict = field(default_factory=dict)  # тег → кількість завдань
    aliased_tags: dict = field(default_factory=dict)  # тег з помилкою → назва конспекту

    @property
    def can_import(self):
        return bool(self.to_add)


def parse_bank_source(source):
    """Текст файлу bank_*.py → (TOPIC_NAME, TASKS). Нічого не виконує."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError, MemoryError) as exc:
        raise BankFormatError(f'Файл не є коректним Python-літералом: {exc}') from exc

    values = {}
    for node in tree.body:
        is_plain_assign = (isinstance(node, ast.Assign) and len(node.targets) == 1
                           and isinstance(node.targets[0], ast.Name))
        if not is_plain_assign:
            raise BankFormatError(
                f'Рядок {node.lineno}: дозволені лише присвоєння TOPIC_NAME = … та TASKS = … '
                f'(файл не виконується, тому доправлення завдань кодом не підтримується).')
        name = node.targets[0].id
        if name not in ('TOPIC_NAME', 'TASKS'):
            raise BankFormatError(f'Рядок {node.lineno}: невідома змінна {name}; очікуються TOPIC_NAME і TASKS.')
        try:
            values[name] = ast.literal_eval(node.value)
        except (ValueError, SyntaxError, TypeError, RecursionError, MemoryError) as exc:
            raise BankFormatError(f'Рядок {node.lineno}: {name} має містити лише літерали ({exc}).') from exc

    if not isinstance(values.get('TOPIC_NAME'), str) or not values['TOPIC_NAME'].strip():
        raise BankFormatError('У файлі немає TOPIC_NAME (непорожнього рядка).')
    if not isinstance(values.get('TASKS'), list):
        raise BankFormatError('У файлі немає TASKS (списку завдань).')
    return values['TOPIC_NAME'].strip(), values['TASKS']


def _is_pair(item, second_type):
    return isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[0], str) \
        and isinstance(item[1], second_type)


def validate_task(task):
    """Список проблем із завданням (порожній — завдання коректне)."""
    if not isinstance(task, dict):
        return ['завдання має бути словником']
    problems = []
    q_type = task.get('type')
    if q_type not in TYPES:
        return [f'невідомий тип «{q_type}» (очікується CHOICE, MATCH або SHORT)']
    if not isinstance(task.get('text'), str) or not task['text'].strip():
        problems.append('порожній текст завдання')
    if task.get('difficulty') not in (1, 2, 3):
        problems.append('складність (difficulty) має бути 1, 2 або 3')
    if not isinstance(task.get('svg_code', ''), str):
        problems.append('svg_code має бути рядком')
    tags = task.get('topic_tags', [])
    if not isinstance(tags, (list, tuple)) or not all(isinstance(t, str) for t in tags):
        problems.append('topic_tags має бути списком рядків')

    options = task.get('options')
    if q_type == 'CHOICE':
        if not isinstance(options, (list, tuple)) or len(options) < 2 or not all(_is_pair(o, bool) for o in options):
            problems.append('options: потрібен список пар (текст, True/False), щонайменше два варіанти')
        else:
            if sum(1 for _, ok in options if ok) != 1:
                problems.append('options: має бути рівно один правильний варіант')
            if any(not text.strip() or len(text) > OPTION_TEXT_MAX for text, _ in options):
                problems.append(f'options: текст варіанта порожній або довший за {OPTION_TEXT_MAX} символів')
    elif q_type == 'MATCH':
        matches = task.get('matches')
        if not isinstance(options, (list, tuple)) or len(options) < 2 or not all(isinstance(o, str) for o in options):
            problems.append('options: потрібен список рядків (варіанти відповідей), щонайменше два')
        elif len(set(options)) != len(options):
            problems.append('options: варіанти не повинні повторюватись')
        elif any(not o.strip() or len(o) > OPTION_TEXT_MAX for o in options):
            problems.append(f'options: текст варіанта порожній або довший за {OPTION_TEXT_MAX} символів')
        if not isinstance(matches, (list, tuple)) or not matches or not all(_is_pair(m, str) for m in matches):
            problems.append('matches: потрібен непорожній список пар (умова, правильний варіант)')
        else:
            if any(len(left) > OPTION_TEXT_MAX for left, _ in matches):
                problems.append(f'matches: умова довша за {OPTION_TEXT_MAX} символів')
            if isinstance(options, (list, tuple)) and any(right not in options for _, right in matches):
                problems.append('matches: правильний варіант відсутній серед options')
    else:  # SHORT
        answer = task.get('answer')
        if not isinstance(answer, (str, int, float)) or isinstance(answer, bool) or not str(answer).strip():
            problems.append('answer: потрібна непорожня відповідь')
        elif len(str(answer)) > SHORT_ANSWER_MAX:
            problems.append(f'answer: довша за {SHORT_ANSWER_MAX} символів')
    return problems


def _normalize(text):
    return ' '.join(str(text).split())


def resolve_material(tag, materials_cache):
    """Конспект для тегу: як у run_import.py (назва містить тег), плюс виправлення відомих помилок у тегах.
    Повертає (конспект або None, назва після виправлення або None, якщо тег не змінювався)."""
    corrected = TAG_ALIASES.get(tag)
    needle = corrected or tag
    if needle not in materials_cache:
        materials_cache[needle] = StudyMaterial.objects.filter(title__icontains=needle).first()
    return materials_cache[needle], corrected


def build_report(topic_name, tasks):
    """Пробний звіт: що буде додано, які завдання вже є (збіг за текстом), які з помилками. База не змінюється."""
    report = ImportReport(topic_name=topic_name, total=len(tasks))
    seen_texts = {_normalize(t) for t in Question.objects.values_list('text', flat=True)}
    materials_cache = {}
    tag_counts = {}

    for index, task in enumerate(tasks, start=1):
        problems = validate_task(task)
        if problems:
            report.errors.append((index, '; '.join(problems)))
            continue
        key = _normalize(task['text'])
        if key in seen_texts:
            report.duplicates.append((index, task['text']))
            continue
        seen_texts.add(key)  # повтор у самому файлі теж дублікат
        report.to_add.append(index)
        for tag in task.get('topic_tags', []):
            material, corrected = resolve_material(tag, materials_cache)
            if corrected:
                report.aliased_tags[tag] = corrected
            if material is None:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
    report.unknown_tags = tag_counts
    return report


@transaction.atomic
def import_tasks(topic_name, tasks):
    """Додає завдання, яких ще немає (логіка як у run_import.py). Повертає (звіт, кількість доданих)."""
    report = build_report(topic_name, tasks)
    if not report.to_add:
        return report, 0

    topic, _ = DiagnosticTopic.objects.get_or_create(name=topic_name)
    materials_cache = {}
    for index in report.to_add:
        data = tasks[index - 1]
        q = Question.objects.create(
            topic=topic,
            question_type=data['type'],
            difficulty=data['difficulty'],
            text=data['text'],
            svg_code=data.get('svg_code', ''),
        )
        for tag in data.get('topic_tags', []):
            material, _ = resolve_material(tag, materials_cache)
            if material:
                q.materials.add(material)

        if data['type'] == 'CHOICE':
            for opt_text, is_correct in data['options']:
                AnswerOption.objects.create(question=q, text=opt_text, is_correct=is_correct)
        elif data['type'] == 'MATCH':
            created = {text: AnswerOption.objects.create(question=q, text=text, is_correct=False)
                       for text in data['options']}
            for left_text, right_text in data['matches']:
                MatchItem.objects.create(question=q, text=left_text, correct_option=created[right_text])
        else:
            q.correct_short_answer = str(data['answer'])
            q.save()
    return report, len(report.to_add)
