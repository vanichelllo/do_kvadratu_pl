import ast
import json
import re
from dataclasses import dataclass, field
from django.db import transaction

# ВИДАЛИЛИ DiagnosticTopic, ДОДАЛИ CurriculumTopic
from .expr import ExprError, parse as parse_expression
from .models import AnswerOption, MatchItem, Question, StudyMaterial, CurriculumTopic

MAX_FILE_BYTES = 2 * 1024 * 1024

TAG_ALIASES = {
    '34. Теореми косинусів та теорема синусів': '34. Теорема косинусів та теорема синусів',
}

TYPES = ('CHOICE', 'MATCH', 'SHORT', 'MULTI', 'TF', 'FIELDS', 'ERROR', 'ORDER', 'GROUP', 'EXPR', 'POINT', 'COORD')
# Ключі завдання, що зберігаються в Question.spec для типів шкільної практики
SPEC_KEYS = {
    'MULTI': ('options',), 'TF': ('statements',), 'FIELDS': ('fields', 'unordered'), 'ERROR': ('steps', 'wrong'),
    'ORDER': ('items',), 'GROUP': ('groups', 'items'), 'EXPR': ('answer', 'vars'),
    'POINT': ('min', 'max', 'step', 'answer'), 'COORD': ('xmin', 'xmax', 'ymin', 'ymax', 'step', 'answer'),
}
SKILLS = ('MODEL', 'SOLVE', 'ANALYZE')
SHORT_ANSWER_MAX = 50
OPTION_TEXT_MAX = 255

class BankFormatError(Exception):
    pass

@dataclass
class ImportReport:
    topic_name: str = ''
    total: int = 0
    to_add: list = field(default_factory=list)
    added: list = field(default_factory=list)
    duplicates: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    unknown_tags: dict = field(default_factory=dict)
    aliased_tags: dict = field(default_factory=dict)

    @property
    def can_import(self):
        return bool(self.to_add)

def parse_bank_source(source):
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError, MemoryError) as exc:
        raise BankFormatError(f'Файл не є коректним Python-літералом: {exc}') from exc

    values = {}
    for node in tree.body:
        is_plain_assign = (isinstance(node, ast.Assign) and len(node.targets) == 1
                           and isinstance(node.targets[0], ast.Name))
        if not is_plain_assign:
            raise BankFormatError('Дозволені лише присвоєння TOPIC_NAME = … та TASKS = …')
        name = node.targets[0].id
        if name not in ('TOPIC_NAME', 'TASKS', 'COURSE', 'GRADE'):
            continue
        try:
            values[name] = ast.literal_eval(node.value)
        except Exception as exc:
            raise BankFormatError(f'Рядок {node.lineno}: {name} має містити лише літерали ({exc}).') from exc

    if not isinstance(values.get('TOPIC_NAME'), str) or not values['TOPIC_NAME'].strip():
        raise BankFormatError('У файлі немає TOPIC_NAME.')
    if not isinstance(values.get('TASKS'), list):
        raise BankFormatError('У файлі немає TASKS.')
    # Шкільний банк (5–11 кл.): COURSE і GRADE однозначно визначають тему — «1.1. …» є в кожному класі.
    # Їх переносимо в кожне завдання, щоб вони збереглися й після об'єднання банків (combine_banks)
    if 'GRADE' in values or 'COURSE' in values:
        course, grade = values.get('COURSE'), values.get('GRADE')
        if not (isinstance(course, str) and course.strip() and isinstance(grade, str) and grade.strip()):
            raise BankFormatError('Для шкільного банку потрібні обидва рядки: COURSE і GRADE.')
        for task in values['TASKS']:
            if isinstance(task, dict):
                task.setdefault('course', course.strip())
                task.setdefault('grade', grade.strip())
    return values['TOPIC_NAME'].strip(), values['TASKS']

def _is_pair(item, second_type):
    return isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[0], str) and isinstance(item[1], second_type)

def validate_task(task):
    if not isinstance(task, dict): return ['завдання має бути словником']
    problems = []
    q_type = task.get('type')
    if q_type not in TYPES: return [f'невідомий тип «{q_type}»']
    if not isinstance(task.get('text'), str) or not task['text'].strip(): problems.append('порожній текст')
    if task.get('difficulty') not in (1, 2, 3): problems.append('складність має бути 1, 2 або 3')
    if 'topic' in task and (not isinstance(task['topic'], str) or not task['topic'].strip()):
        problems.append('topic: має бути назвою теми, напр. «21. Показникові рівняння»')
    if task.get('skill', 'SOLVE') not in SKILLS:
        problems.append('skill: має бути MODEL, SOLVE або ANALYZE')
    for text_field in ('hint', 'solution'):
        if not isinstance(task.get(text_field, ''), str):
            problems.append(f'{text_field}: має бути текстом')
    if 'grade' in task and not (isinstance(task.get('grade'), str) and isinstance(task.get('course'), str)):
        problems.append('grade/course: мають бути назвами класу й курсу')
    options = task.get('options')
    if q_type == 'CHOICE':
        if not isinstance(options, (list, tuple)) or len(options) < 2 or not all(_is_pair(o, bool) for o in options):
            problems.append('options: помилка формату CHOICE')
        elif sum(1 for _, ok in options if ok) != 1:
            problems.append('options: має бути рівно один правильний варіант')
    elif q_type == 'MATCH':
        matches = task.get('matches')
        if not isinstance(options, (list, tuple)) or len(options) < 2: problems.append('options: помилка MATCH')
        if not isinstance(matches, (list, tuple)) or not matches: problems.append('matches: помилка MATCH')
    elif q_type == 'SHORT':
        if not str(task.get('answer', '')).strip(): problems.append('answer: порожня відповідь')
    else:
        problems += validate_school_spec(q_type, task)
    return problems


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _on_grid(value, start, step):
    k = (value - start) / step
    return abs(k - round(k)) < 1e-9


def _texts(value, minimum=2):
    return isinstance(value, (list, tuple)) and len(value) >= minimum and all(isinstance(v, str) and v.strip() for v in value)


def validate_school_spec(q_type, task):
    """Перевірка даних нових типів (кілька правильних, так/ні, поля, кроки, порядок, групи, вираз, точки)."""
    if q_type == 'MULTI':
        options = task.get('options')
        if not isinstance(options, (list, tuple)) or len(options) < 2 or not all(_is_pair(o, bool) for o in options):
            return ['options: список пар (текст, True/False)']
        return [] if any(ok for _, ok in options) else ['options: потрібен хоча б один правильний варіант']
    if q_type == 'TF':
        statements = task.get('statements')
        if not isinstance(statements, (list, tuple)) or not statements or not all(_is_pair(s, bool) for s in statements):
            return ['statements: список пар (твердження, True/False)']
        return []
    if q_type == 'FIELDS':
        fields = task.get('fields')
        if not isinstance(fields, (list, tuple)) or not fields or not all(
                isinstance(f, (list, tuple)) and len(f) == 2 and isinstance(f[0], str) and str(f[1]).strip() for f in fields):
            return ['fields: список пар (підпис поля, відповідь)']
        return []
    if q_type == 'ERROR':
        steps, wrong = task.get('steps'), task.get('wrong')
        if not _texts(steps):
            return ['steps: щонайменше 2 кроки розв\'язання']
        if not (isinstance(wrong, int) and not isinstance(wrong, bool) and 0 <= wrong < len(steps)):
            return ['wrong: номер хибного кроку, рахуючи з 0']
        return []
    if q_type == 'ORDER':
        return [] if _texts(task.get('items')) else ['items: щонайменше 2 елементи в правильному порядку']
    if q_type == 'GROUP':
        groups, items = task.get('groups'), task.get('items')
        if not _texts(groups):
            return ['groups: щонайменше 2 назви груп']
        if not isinstance(items, (list, tuple)) or len(items) < 2 or not all(
                _is_pair(i, int) and 0 <= i[1] < len(groups) for i in items):
            return ['items: список пар (елемент, номер групи з 0)']
        return []
    if q_type == 'EXPR':
        variables = task.get('vars', [])
        if not isinstance(variables, (list, tuple)) or not all(isinstance(v, str) and len(v) == 1 and v.isalpha() for v in variables):
            return ['vars: список однолітерних змінних, напр. ["a", "b"]']
        try:
            parse_expression(task.get('answer', ''), variables)
        except ExprError as exc:
            return [f'answer: вираз не розібрано ({exc})']
        return []
    if q_type == 'POINT':
        values = [task.get(k) for k in ('min', 'max', 'step', 'answer')]
        if not all(_is_number(v) for v in values) or not values[0] <= values[3] <= values[1] or values[2] <= 0 \
                or values[0] >= values[1]:
            return ['min, max, step, answer: числа, min ≤ answer ≤ max, step > 0']
        if not _on_grid(values[3], values[0], values[2]):
            return ['answer: точка має лежати на поділці (min + k·step)']
        return []
    if q_type == 'COORD':
        bounds = [task.get(k) for k in ('xmin', 'xmax', 'ymin', 'ymax')]
        answer, step = task.get('answer'), task.get('step', 1)
        if not all(_is_number(v) for v in bounds) or bounds[0] >= bounds[1] or bounds[2] >= bounds[3] \
                or not _is_number(step) or step <= 0:
            return ['xmin, xmax, ymin, ymax, step: числа, min < max, step > 0']
        if not (isinstance(answer, (list, tuple)) and len(answer) == 2 and all(_is_number(v) for v in answer)
                and bounds[0] <= answer[0] <= bounds[1] and bounds[2] <= answer[1] <= bounds[3]):
            return ['answer: точка (x, y) у межах площини']
        if not (_on_grid(answer[0], bounds[0], step) and _on_grid(answer[1], bounds[2], step)):
            return ['answer: точка має лежати у вузлі сітки (min + k·step)']
        return []
    return []


def task_spec(task):
    spec = {}
    for key in SPEC_KEYS.get(task['type'], ()):
        if key in task:
            value = task[key]
            spec[key] = [list(v) if isinstance(v, tuple) else v for v in value] if isinstance(value, (list, tuple)) else value
    return spec

def _normalize(text):
    return ' '.join(str(text).split())


def _key(text, options=(), lefts=(), answer=''):
    # Повтор — це той самий текст І ті самі варіанти/пари/відповідь: загальні умови на кшталт
    # «Узгодьте вираз (1–3) із …» повторюються в різних завданнях з різним змістом
    return (_normalize(text), tuple(sorted(map(_normalize, options))), tuple(sorted(map(_normalize, lefts))),
            _normalize(answer or ''))


def task_key(task):
    if task.get('type') in SPEC_KEYS:
        return _key(task['text'], [json.dumps(task_spec(task), sort_keys=True, ensure_ascii=False)])
    options = task.get('options') or []
    if task.get('type') == 'CHOICE':
        options = [text for text, _ in options]
    return _key(task['text'], options, [left for left, _ in task.get('matches') or []],
                task.get('answer', '') if task.get('type') == 'SHORT' else '')


def question_key(question):
    if question.question_type in SPEC_KEYS:
        return _key(question.text, [json.dumps(question.spec, sort_keys=True, ensure_ascii=False)])
    return _key(question.text, [o.text for o in question.options.all()],
                [m.text for m in question.match_items.all()], question.correct_short_answer)

def resolve_material(tag, materials_cache):
    corrected = TAG_ALIASES.get(tag)
    needle = corrected or tag
    if needle not in materials_cache:
        materials_cache[needle] = StudyMaterial.objects.filter(title__icontains=needle).first()
    return materials_cache[needle], corrected

def school_topic(task, topic_name):
    """Тема шкільного курсу за назвою, класом і курсом; None — якщо такої немає в класифікаторі."""
    return (CurriculumTopic.objects
            .filter(name=(task.get('topic') or topic_name).strip(), chapter__grade__name=task['grade'],
                    chapter__grade__subject__name=task['course'])
            .first())


def build_report(topic_name, tasks):
    report = ImportReport(topic_name=topic_name, total=len(tasks))
    seen = {question_key(q) for q in Question.objects.prefetch_related('options', 'match_items')}
    materials_cache = {}
    tag_counts = {}

    for index, task in enumerate(tasks, start=1):
        problems = validate_task(task)
        if not problems and 'grade' in task and school_topic(task, topic_name) is None:
            problems = [f"тему «{task.get('topic') or topic_name}» не знайдено в «{task['course']} / {task['grade']}»"]
        if problems:
            report.errors.append((index, '; '.join(problems)))
            continue
        key = task_key(task)
        if key in seen:
            report.duplicates.append((index, task['text']))
            continue
        seen.add(key)
        report.to_add.append(index)
        report.added.append((index, task.get('topic') or topic_name, task['text']))
        for tag in task.get('topic_tags', []):
            material, corrected = resolve_material(tag, materials_cache)
            if corrected: report.aliased_tags[tag] = corrected
            if material is None: tag_counts[tag] = tag_counts.get(tag, 0) + 1
    report.unknown_tags = tag_counts
    return report

@transaction.atomic
def import_tasks(topic_name, tasks):
    report = build_report(topic_name, tasks)
    if not report.to_add:
        return report, 0

    # Тема — за номером на початку назви: «21. …» → тема 21 курсу НМТ. У файлі з кількома темами
    # (наприклад, усі банки разом) тема вказана в самому завданні полем "topic"
    nmt_topics = {}
    for nt in CurriculumTopic.objects.filter(chapter__grade__subject__name="Підготовка до НМТ / ЗНО"):
        nt_match = re.match(r'^(\d+)', nt.name)
        if nt_match:
            nmt_topics.setdefault(int(nt_match.group(1)), nt)

    def topic_for(name):
        match = re.match(r'^(\d+)', name)
        return nmt_topics.get(int(match.group(1))) if match else None

    materials_cache = {}
    for index in report.to_add:
        data = tasks[index - 1]
        
        # ЗБЕРІГАЄМО З НОВИМ curriculum_topic
        topic = school_topic(data, topic_name) if 'grade' in data else topic_for(data.get('topic') or topic_name)
        q = Question.objects.create(
            curriculum_topic=topic,
            question_type=data['type'],
            difficulty=data['difficulty'],
            text=data['text'],
            svg_code=data.get('svg_code', ''),
            nush_skill=data.get('skill', 'SOLVE'),
            hint=data.get('hint', ''),
            solution=data.get('solution', ''),
            spec=task_spec(data),
        )
        if 'grade' in data:
            # Шкільне завдання належить усім урокам цієї теми
            q.materials.add(*StudyMaterial.objects.filter(curriculum_topic=topic))

        for tag in data.get('topic_tags', []):
            material, _ = resolve_material(tag, materials_cache)
            if material:
                q.materials.add(material)

        if data['type'] == 'CHOICE':
            for opt_text, is_correct in data['options']:
                AnswerOption.objects.create(question=q, text=opt_text, is_correct=is_correct)
        elif data['type'] == 'MATCH':
            created = {text: AnswerOption.objects.create(question=q, text=text, is_correct=False) for text in data['options']}
            for left_text, right_text in data['matches']:
                MatchItem.objects.create(question=q, text=left_text, correct_option=created[right_text])
        elif data['type'] == 'SHORT':
            q.correct_short_answer = str(data['answer'])
            q.save()
            
    return report, len(report.to_add)