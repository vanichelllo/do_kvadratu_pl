"""Перевірка одного уроку тими самими правилами, що й на сайті (без бази даних).

    python3 check_lesson.py content/school/math-5/1.4.html content/school/math-5/bank_1.4.py
"""
import os, re, sys, warnings
from collections import Counter
REPO = '/home/user/do_kvadratu_pl'
sys.path.insert(0, REPO)
os.environ.setdefault('SECRET_KEY', 'check-only')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'do_kvadratu.settings')
import django; django.setup()
from materials.bank_import import parse_bank_source
from materials.content_check import check_bank, check_presentation

import json
html_path = sys.argv[1]
bank_path = sys.argv[2] if len(sys.argv) > 2 else None
meta = json.load(open(os.path.join(os.path.dirname(html_path), 'meta.json'), encoding='utf-8'))
grade = int(meta['grade'].split()[0])
profile = 'A' if grade <= 6 else 'B' if grade <= 9 else 'V'
ok = True
html = open(html_path, encoding='utf-8').read()
problems, warns = check_presentation(html)
print(f'== {html_path}')
for p in problems: print('  ПОМИЛКА:', p); ok = False
for w in warns: print('  увага:', w); ok = False
if meta['course'] not in html:
    print(f"  ПОМИЛКА: у шапці немає назви курсу «{meta['course']}»"); ok = False
if bank_path is None:
    print('ГОТОВО: усе чисто' if ok else 'Є ЗАУВАЖЕННЯ — виправте й запустіть знову')
    sys.exit(0 if ok else 1)

print(f'== {bank_path}')
source = open(bank_path, encoding='utf-8').read()
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter('always')
    compile(source, bank_path, 'exec')
for w in caught:
    print(f'  ПОМИЛКА: рядок {w.lineno}: {w.message} — рядки з \\ записуйте як r"..."'); ok = False
name, tasks = parse_bank_source(source)
problems, warns = check_bank(tasks, profile)
for p in problems: print('  ПОМИЛКА:', p); ok = False
for w in warns: print('  увага:', w); ok = False

tree = open(os.path.join(REPO, 'docs/lesson_prompt.md'), encoding='utf-8').read()
chapters = re.findall(r'^- \*\*(.+?)\*\*$', tree, flags=re.M)
lessons = re.findall(r'^  - (.+)$', tree, flags=re.M)
valid = set(lessons) | {f'Узагальнення: {c}' for c in chapters}
if name not in valid:
    print(f'  ПОМИЛКА: TOPIC_NAME «{name}» не збігається дослівно з деревом тем'); ok = False
values = dict(re.findall(r'^(COURSE|GRADE) = "(.+)"$', source, flags=re.M))
if values != {'COURSE': meta['course'], 'GRADE': meta['grade']}:
    print(f'  ПОМИЛКА: COURSE / GRADE: {values}'); ok = False

cells = Counter((t.get('difficulty'), t.get('skill')) for t in tasks)
types = Counter(t.get('type') for t in tasks)
print(f'  завдань: {len(tasks)}; сходинки×критерії: {dict(sorted(cells.items()))}')
print(f'  типи: {dict(types)}')
for level in (1, 2, 3):
    for skill in ('MODEL', 'SOLVE', 'ANALYZE'):
        if cells[(level, skill)] != 5:
            print(f'  ПОМИЛКА: сходинка {level} × {skill}: {cells[(level, skill)]} (потрібно рівно 5)'); ok = False
if sum(1 for t in tasks if t.get('difficulty') == 4) != 5 or sum(1 for t in tasks if t.get('difficulty') == 5) != 2:
    print('  ПОМИЛКА: потрібно 5 босів (difficulty 4) і 2 ультра-боси (difficulty 5)'); ok = False
print('ГОТОВО: усе чисто' if ok else 'Є ЗАУВАЖЕННЯ — виправте й запустіть знову')
sys.exit(0 if ok else 1)
