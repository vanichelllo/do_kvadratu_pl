import ast
import re
from dataclasses import dataclass, field
from django.db import transaction

# ВИДАЛИЛИ DiagnosticTopic, ДОДАЛИ CurriculumTopic
from .models import AnswerOption, MatchItem, Question, StudyMaterial, CurriculumTopic

MAX_FILE_BYTES = 2 * 1024 * 1024

TAG_ALIASES = {
    '34. Теореми косинусів та теорема синусів': '34. Теорема косинусів та теорема синусів',
}

TYPES = ('CHOICE', 'MATCH', 'SHORT')
SHORT_ANSWER_MAX = 50
OPTION_TEXT_MAX = 255

class BankFormatError(Exception):
    pass

@dataclass
class ImportReport:
    topic_name: str = ''
    total: int = 0
    to_add: list = field(default_factory=list)
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
        if name not in ('TOPIC_NAME', 'TASKS'):
            continue
        try:
            values[name] = ast.literal_eval(node.value)
        except Exception as exc:
            raise BankFormatError(f'Помилка читання {name}: {exc}') from exc

    if not isinstance(values.get('TOPIC_NAME'), str) or not values['TOPIC_NAME'].strip():
        raise BankFormatError('У файлі немає TOPIC_NAME.')
    if not isinstance(values.get('TASKS'), list):
        raise BankFormatError('У файлі немає TASKS.')
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
    else:
        if not str(task.get('answer', '')).strip(): problems.append('answer: порожня відповідь')
    return problems

def _normalize(text):
    return ' '.join(str(text).split())

def resolve_material(tag, materials_cache):
    corrected = TAG_ALIASES.get(tag)
    needle = corrected or tag
    if needle not in materials_cache:
        materials_cache[needle] = StudyMaterial.objects.filter(title__icontains=needle).first()
    return materials_cache[needle], corrected

def build_report(topic_name, tasks):
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
        seen_texts.add(key)
        report.to_add.append(index)
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

    # === НОВА ЛОГІКА: Шукаємо CurriculumTopic замість DiagnosticTopic ===
    target_topic = None
    match = re.match(r'^(\d+)', topic_name)
    if match:
        topic_num = int(match.group(1))
        # Шукаємо тему НМТ з таким самим номером
        for nt in CurriculumTopic.objects.filter(chapter__grade__subject__name="Підготовка до НМТ / ЗНО"):
            nt_match = re.match(r'^(\d+)', nt.name)
            if nt_match and int(nt_match.group(1)) == topic_num:
                target_topic = nt
                break

    materials_cache = {}
    for index in report.to_add:
        data = tasks[index - 1]
        
        # ЗБЕРІГАЄМО З НОВИМ curriculum_topic
        q = Question.objects.create(
            curriculum_topic=target_topic,
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
            created = {text: AnswerOption.objects.create(question=q, text=text, is_correct=False) for text in data['options']}
            for left_text, right_text in data['matches']:
                MatchItem.objects.create(question=q, text=left_text, correct_option=created[right_text])
        else:
            q.correct_short_answer = str(data['answer'])
            q.save()
            
    return report, len(report.to_add)