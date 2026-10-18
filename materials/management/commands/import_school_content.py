"""Завантажує на сайт шкільний контент класу з папки репозиторію (напр. content/school/math-5):

    meta.json        {"course": "Математика (5-6 класи)", "grade": "5 клас"}
    1.1.html         презентація теми «1.1. …»
    summary-1.html   презентація-узагальнення розділу «Розділ 1. …»
    bank_1.1.py      банк завдань (формат docs/bank_prompt.md)

Кожен файл спершу перевіряється (materials/content_check.py); файл із помилками пропускається.
Презентація стає html_content уроку теми (урок створюється, якщо його ще немає). Завдання з банків додаються
без дублікатів. Без --publish уроки лишаються неопублікованими (видно вам і репетиторам за підпискою).

    python manage.py import_school_content content/school/math-5 --check     # лише перевірити
    python manage.py import_school_content content/school/math-5 --price 49  # завантажити
    python manage.py import_school_content --all --keep-going                # усі класи (так робить деплой)

Деплой (build.sh) запускає команду з --all --keep-going: усе, що злито в main, саме з'являється на сайті.
Файл із помилками пропускається й не зупиняє деплой. Презентація перезаписується, лише якщо файл змінився.
"""
import json
import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from materials.bank_import import BankFormatError, build_report, import_tasks, parse_bank_source
from materials.content_check import check_bank, check_presentation
from materials.models import CurriculumTopic, StudyMaterial


class Command(BaseCommand):
    help = 'Перевіряє й завантажує презентації та банки завдань шкільного класу з папки контенту'

    def add_arguments(self, parser):
        parser.add_argument('folders', nargs='*')
        parser.add_argument('--all', dest='all_folders', action='store_true', help='Усі папки з content/school')
        parser.add_argument('--keep-going', action='store_true',
                            help='Не зупинятися з помилкою (для деплою): лише вивести, які файли пропущено')
        parser.add_argument('--check', action='store_true', help='Лише перевірити, нічого не записувати')
        parser.add_argument('--publish', action='store_true', help='Опублікувати уроки на вітрині')
        parser.add_argument('--price', type=int, default=None, help='Ціна нових уроків, грн (за замовчуванням 0)')

    def handle(self, folders, all_folders=False, keep_going=False, check=False, publish=False, price=None, **options):
        roots = [Path(folder) for folder in folders]
        if all_folders:
            roots += sorted(p for p in (Path(settings.BASE_DIR) / 'content' / 'school').iterdir() if p.is_dir())
        if not roots:
            raise CommandError('Вкажіть папку класу або --all')
        failed = 0
        for root in roots:
            self.stdout.write(self.style.MIGRATE_HEADING(str(root)))
            try:
                failed += self.import_folder(root, check, publish, price)
            except CommandError as exc:
                if not keep_going:
                    raise
                self.stdout.write(self.style.ERROR(f'   помилка: {exc}'))
                failed += 1
        if failed and not keep_going:
            raise CommandError(f'Файлів з помилками: {failed} — їх пропущено.')
        if failed:
            self.stdout.write(self.style.WARNING(f'Файлів з помилками: {failed} — їх пропущено.'))
        else:
            self.stdout.write(self.style.SUCCESS('Готово.' if not check else 'Перевірку пройдено.'))

    def import_folder(self, root, check, publish, price):
        """Перевіряє й завантажує одну папку класу; повертає кількість файлів з помилками."""
        meta_path = root / 'meta.json'
        if not meta_path.exists():
            raise CommandError(f'Немає {meta_path}')
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
        topics = CurriculumTopic.objects.filter(chapter__grade__name=meta['grade'],
                                                chapter__grade__subject__name=meta['course'])
        if not topics.exists():
            raise CommandError(f'У класифікаторі немає «{meta["course"]} / {meta["grade"]}» — спершу import_curriculum')
        profile = 'A' if meta['grade'].startswith(('5', '6')) else 'B'
        failed = 0

        for path in sorted(root.glob('*.html'), key=lambda p: natural_key(p.stem)):
            topic = self.topic_for(path.stem, topics)
            problems, warnings = check_presentation(path.read_text(encoding='utf-8'))
            failed += self.report(path.name, problems, warnings, topic)
            if problems or topic is None or check:
                continue
            html = path.read_text(encoding='utf-8')
            with transaction.atomic():
                material = StudyMaterial.objects.filter(curriculum_topic=topic, is_bundle=False).first()
                if material is None:
                    material = StudyMaterial(curriculum_topic=topic, title=topic.name, price=price or 0,
                                             is_free=not price)
                elif material.html_content == html and (not publish or material.is_published):
                    continue   # нічого не змінилося — повторний деплой не чіпає урок
                material.html_content = html
                if publish:
                    material.is_published = True
                material.save()
                self.stdout.write(f'   → презентацію записано: {topic.name}')

        for path in sorted(root.glob('bank_*.py'), key=lambda p: natural_key(p.stem)):
            try:
                topic_name, tasks = parse_bank_source(path.read_text(encoding='utf-8'))
            except BankFormatError as exc:
                failed += self.report(path.name, [str(exc)], [], None)
                continue
            problems, warnings = check_bank(tasks, profile)
            report = build_report(topic_name, tasks)
            problems += [f'№{i}: {message}' for i, message in report.errors if not any(
                p.startswith(f'№{i}:') for p in problems)]
            failed += self.report(path.name, problems, warnings, True,
                                  extra=f'нових {len(report.to_add)}, дублікатів {len(report.duplicates)}')
            if problems or check:
                continue
            added = import_tasks(topic_name, tasks)[1]
            self.stdout.write(f'   → додано завдань: {added}')

        return failed

    def topic_for(self, stem, topics):
        summary = re.fullmatch(r'summary-(\d+)', stem)
        if summary:
            return topics.filter(kind='summary', chapter__name__startswith=f'Розділ {summary.group(1)}.').first()
        return topics.filter(kind='lesson', name__startswith=f'{stem}. ').first()

    def report(self, name, problems, warnings, topic, extra=''):
        if topic is None:
            problems = problems + ['не знайдено відповідну тему в класифікаторі']
        status = self.style.ERROR('✗') if problems else self.style.SUCCESS('✓')
        self.stdout.write(f'{status} {name}{" — " + extra if extra else ""}')
        for problem in problems:
            self.stdout.write(self.style.ERROR(f'   помилка: {problem}'))
        for warning in warnings:
            self.stdout.write(self.style.WARNING(f'   увага: {warning}'))
        return 1 if problems else 0


def natural_key(stem):
    return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', stem)]
