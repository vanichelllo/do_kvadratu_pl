"""Перевірка шкільного контенту перед завантаженням на сайт: презентації (вимоги docs/html_prompt.md, розділ 4)
і банки завдань (склад за docs/bank_prompt.md). Помилки (problems) блокують імпорт файлу; попередження (warnings)
лише показуються — наприклад, банк менший за рекомендований.
"""
import re
from collections import Counter

from .bank_import import validate_task

REQUIRED_IDS = ('btn-theme', 'btn-fullscreen', 'progress-bar', 'slide-counter', 'btn-prev', 'btn-next')
REQUIRED_CLASSES = ('navbar', 'brand-logo-container', 'presentation-viewport', 'slide-card', 'controls-footer')
FORBIDDEN = {
    'localStorage': 'localStorage заборонено',
    'sessionStorage': 'sessionStorage заборонено',
    'alert(': 'alert() заборонено',
    'prompt(': 'prompt() заборонено',
    'fetch(': 'fetch() заборонено',
    'window.open': 'відкриття нових вікон заборонено',
    '<img': 'зображення <img> заборонені — лише вбудований SVG',
    'base64,': 'base64 заборонено',
}
ALLOWED_SCRIPT = 'https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js'
MAX_BYTES = 100 * 1024

BANK_SIZE = 45            # рекомендовано: по 15 на сходинку
MIN_PER_CELL = 3          # мінімум завдань на «сходинку × критерій», щоб практика могла чергувати критерії
MAX_CHOICE_SHARE = 0.4
MIN_TYPES = 6


def check_presentation(html):
    """(problems, warnings) для HTML-презентації."""
    problems, warnings = [], []
    if len(html.encode('utf-8')) > MAX_BYTES:
        problems.append(f'файл більший за {MAX_BYTES // 1024} КБ')
    if not html.lstrip().lower().startswith('<!doctype html>') or '</html>' not in html.lower():
        problems.append('файл має починатися з <!DOCTYPE html> і закінчуватися </html>')
    if '</head>' not in html:
        problems.append('немає </head> — сайт вставляє туди свої стилі')
    for element_id in REQUIRED_IDS:
        if f'id="{element_id}"' not in html:
            problems.append(f'немає службового id="{element_id}"')
    for cls in REQUIRED_CLASSES:
        if not re.search(rf'class="[^"]*\b{re.escape(cls)}\b', html):
            problems.append(f'немає службового класу «{cls}»')
    if 'class="slide-card active"' not in html:
        problems.append('перший слайд має мати клас «slide-card active»')
    if "addEventListener('keydown'" not in html and 'addEventListener("keydown"' not in html:
        problems.append('немає обробника keydown — кнопки сайту не гортатимуть слайди')
    if 'goToSlide' not in html:
        problems.append('немає функції goToSlide')
    for needle, message in FORBIDDEN.items():
        if needle in html:
            problems.append(message)
    for src in re.findall(r'<script[^>]+src="([^"]+)"', html):
        if src != ALLOWED_SCRIPT:
            problems.append(f'зовнішній скрипт заборонено: {src}')
    for href in re.findall(r'<link[^>]+href="(https?://[^"]+)"', html):
        problems.append(f'зовнішній ресурс заборонено: {href}')
    if re.search(r'href="https?://', html):
        warnings.append('є посилання на інші сайти')
    # Знаки < і > у формулах ламають розмітку — мають бути \lt і \gt
    for formula in re.findall(r'\$([^$]+)\$', re.sub(r'<script.*?</script>', '', html, flags=re.S)):
        if re.search(r'[<>]', formula) and not re.search(r'</?[a-z]', formula):
            problems.append(f'у формулі «${formula[:40]}$» є < або > — пишіть \\lt / \\gt')
            break
    slides = len(re.findall(r'class="slide-card[ "]', html))
    if not 5 <= slides <= 10:   # 5–9 за профілем + підсумковий слайд «Коротко про тему»
        warnings.append(f'слайдів {slides} (за методикою 5–10)')
    return problems, warnings


def check_bank(tasks, profile='A'):
    """(problems, warnings) для списку завдань банку. profile — методичний профіль класу (A — 5–6 кл.)."""
    problems, warnings = [], []
    for index, task in enumerate(tasks, start=1):
        for problem in validate_task(task):
            problems.append(f'№{index}: {problem}')
        if not isinstance(task, dict):
            continue
        if not str(task.get('solution', '')).strip():
            problems.append(f'№{index}: немає розв\'язання (solution)')
        if profile == 'A' and not str(task.get('hint', '')).strip():
            problems.append(f'№{index}: для 5–6 класів потрібна підказка (hint)')
        if profile == 'A' and task.get('type') == 'MATCH':
            problems.append(f'№{index}: MATCH не використовується в 5–6 класах')
    valid = [t for t in tasks if isinstance(t, dict)]
    if len(valid) < BANK_SIZE:
        warnings.append(f'завдань {len(valid)}, рекомендовано {BANK_SIZE}')
    cells = Counter((t.get('difficulty'), t.get('skill', 'SOLVE')) for t in valid)
    for level in (1, 2, 3):
        for skill in ('MODEL', 'SOLVE', 'ANALYZE'):
            if cells[(level, skill)] < MIN_PER_CELL:
                warnings.append(f'сходинка {level}, критерій {skill}: {cells[(level, skill)]} завд. '
                                f'(потрібно щонайменше {MIN_PER_CELL})')
    types = Counter(t.get('type') for t in valid)
    if valid and types['CHOICE'] / len(valid) > MAX_CHOICE_SHARE:
        warnings.append(f'CHOICE {types["CHOICE"]} з {len(valid)} — більше {int(MAX_CHOICE_SHARE * 100)} %')
    if len(types) < MIN_TYPES:
        warnings.append(f'типів завдань {len(types)}, рекомендовано щонайменше {MIN_TYPES}')
    for index, task in enumerate(tasks, start=1):
        if isinstance(task, dict) and not validate_task(task) and not answer_is_accepted(task):
            problems.append(f'№{index}: сайт не зарахує правильну відповідь — перевірте дані завдання')
    texts = Counter(' '.join(str(t.get('text', '')).split()) for t in valid)
    for text, count in texts.items():
        if count > 1 and len(text) > 30:   # короткі загальні умови («Правда чи ні?») повторюються природно
            warnings.append(f'однаковий текст завдання ×{count}: «{text[:50]}»')
    return problems, warnings


def answer_is_accepted(task):
    """Чи перевірка на сайті зарахує правильну відповідь з самого банку (наприклад, відповідь у FIELDS
    записана так, що не розбирається, або точка поза поділками)."""
    from .models import Question
    from .practice import is_correct
    from .bank_import import task_spec
    q_type = task['type']
    if q_type in ('CHOICE', 'MATCH'):
        return True   # перевіряються структурою варіантів у validate_task
    spec = task_spec(task)
    question = Question(question_type=q_type, text=task['text'], spec=spec,
                        correct_short_answer=str(task.get('answer', '')) if q_type == 'SHORT' else None)
    expected = {
        'SHORT': lambda: str(task.get('answer', '')),
        'MULTI': lambda: [i for i, (_, ok) in enumerate(spec.get('options', [])) if ok],
        'TF': lambda: [bool(ok) for _, ok in spec.get('statements', [])],
        'FIELDS': lambda: [str(v) for _, v in spec.get('fields', [])],
        'ERROR': lambda: spec.get('wrong'),
        'ORDER': lambda: list(range(len(spec.get('items', [])))),
        'GROUP': lambda: [g for _, g in spec.get('items', [])],
        'EXPR': lambda: str(spec.get('answer', '')),
        'POINT': lambda: float(spec.get('answer', 0)),
        'COORD': lambda: [float(v) for v in spec.get('answer', [0, 0])],
    }[q_type]()
    return is_correct(question, expected)

