import os
import re
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from materials.models import StudyMaterial


class Command(BaseCommand):
    help = 'Автоматично імпортує 46 конспектів з папки import_files'

    def handle(self, *args, **options):
        folder_path = os.path.join(settings.BASE_DIR, 'import_files')

        if not os.path.exists(folder_path):
            self.stdout.write(self.style.ERROR(f'Папку {folder_path} не знайдено!'))
            return

        # СЛОВНИК ЦІН: вкажіть номер матеріалу та його ціну.
        # Усі, кого немає в цьому списку, автоматично стануть безкоштовними (0 грн).
        PRICES_MAP = {
            2: 19,
            3: 19,
            # Додайте сюди інші платні номери за аналогією:
            # 4: 29,
            # 5: 29,
        }

        files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
        self.stdout.write(self.style.SUCCESS(f'Знайдено {len(files)} файлів для імпорту.'))

        count = 0
        for file_name in files:
            # Витягуємо номер конспекту з початку назви файлу
            match = re.match(r'^(\d+)', file_name)
            if not match:
                continue

            file_number = int(match.group(1))

            # Очищаємо назву матеріалу від розширення .pdf для гарного відображення на вітрині
            title = os.path.splitext(file_name)[0]

            # Визначаємо ціну: якщо номера немає в словнику — ставимо 0
            price = PRICES_MAP.get(file_number, 0)

            # Перевіряємо, чи такий матеріал уже є в базі, щоб не дублювати
            if StudyMaterial.objects.filter(title=title).exists():
                self.stdout.write(self.style.WARNING(f'«{title}» вже є в базі, пропускаємо.'))
                continue

            full_file_path = os.path.join(folder_path, file_name)

            # Створюємо об'єкт у базі даних
            material = StudyMaterial(
                title=title,
                price=price,
                is_published=True
            )

            # Безпечно відкриваємо і прив'язуємо фізичний PDF-файл до моделі Django
            with open(full_file_path, 'rb') as f:
                material.file.save(file_name, File(f), save=True)

            count += 1
            self.stdout.write(self.style.SUCCESS(f'Успішно імпортовано: {title} ({price} грн)'))

        self.stdout.write(self.style.SUCCESS(f'Роботу завершено! Додано нових матеріалів: {count}'))