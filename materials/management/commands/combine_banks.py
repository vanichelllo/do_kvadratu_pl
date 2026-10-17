import glob
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from materials.bank_import import parse_bank_source


class Command(BaseCommand):
    help = ('Збирає всі import_files/bank_*.py в один файл для завантаження в адмінці '
            '(«Завдання → Завантажити завдання»). Тема кожного завдання зберігається в полі "topic".')

    def add_arguments(self, parser):
        parser.add_argument('output', nargs='?', default='all_banks.py', help='Куди записати файл')

    def handle(self, *args, **options):
        tasks = []
        for path in sorted(glob.glob(os.path.join(settings.BASE_DIR, 'import_files', 'bank_*.py'))):
            with open(path, encoding='utf-8') as f:
                topic_name, bank_tasks = parse_bank_source(f.read())
            tasks += [{**task, 'topic': task.get('topic') or topic_name} for task in bank_tasks]

        with open(options['output'], 'w', encoding='utf-8') as out:
            out.write('# Згенеровано командою combine_banks з import_files/bank_*.py — правте самі банки, не цей файл\n')
            out.write('TOPIC_NAME = "Усі банки завдань"\nTASKS = [\n')
            out.writelines(f'    {task!r},\n' for task in tasks)
            out.write(']\n')
        size_mb = os.path.getsize(options['output']) / (1024 * 1024)
        self.stdout.write(self.style.SUCCESS(f'Записано {len(tasks)} завдань у {options["output"]} ({size_mb:.1f} МБ).'))
