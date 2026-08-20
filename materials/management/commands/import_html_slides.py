import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from materials.models import StudyMaterial


class Command(BaseCommand):
    help = 'Автоматичний імпорт HTML презентацій з папки import_html'

    def handle(self, *args, **kwargs):
        html_dir = os.path.join(settings.BASE_DIR, 'import_files', 'import_html')

        if not os.path.exists(html_dir):
            self.stdout.write(self.style.ERROR(f"Папку {html_dir} не знайдено. Створіть її та додайте файли."))
            return

        # Беремо лише поодинокі теми (не пакети)
        materials = StudyMaterial.objects.filter(is_bundle=False)
        success_count = 0

        for material in materials:
            # Шукаємо число на початку назви конспекту (напр. "1. Числові множини" -> 1)
            match = re.match(r'^(\d+)', material.title)
            if match:
                topic_num = match.group(1)
                html_filename = f"{topic_num}.html"
                html_path = os.path.join(html_dir, html_filename)

                if os.path.exists(html_path):
                    with open(html_path, 'r', encoding='utf-8') as f:
                        material.html_content = f.read()
                        material.save()
                        self.stdout.write(self.style.SUCCESS(f"✅ Додано HTML для: {material.title}"))
                        success_count += 1
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ Файл {html_filename} не знайдено для {material.title}"))

        self.stdout.write(self.style.SUCCESS(f"Імпорт успішно завершено! Оновлено матеріалів: {success_count}."))