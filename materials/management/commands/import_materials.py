import os
from django.core.management.base import BaseCommand
from django.core.files import File
from openpyxl import load_workbook

# Імпортуємо модель з вашого додатку materials
from materials.models import StudyMaterial


class Command(BaseCommand):
    help = 'Примусове завантаження матеріалів з Excel-матриці'

    def handle(self, *args, **kwargs):
        excel_path = 'matrix.xlsx'
        pdf_folder = 'import_files'

        if not os.path.exists(excel_path):
            self.stdout.write(self.style.ERROR(f'Файл {excel_path} не знайдено!'))
            return

        wb = load_workbook(excel_path)
        ws = wb.active

        self.stdout.write(f"Починаємо імпорт {ws.max_row - 1} матеріалів...")

        # Пропускаємо перший рядок (заголовки)
        for row in ws.iter_rows(min_row=2, values_only=True):
            title, price, filename, is_free, is_bundle = row

            if not title or not filename:
                continue

            pdf_path = os.path.join(pdf_folder, filename)

            if not os.path.exists(pdf_path):
                self.stdout.write(self.style.WARNING(f'Пропущено: файл не знайдено ({pdf_path})'))
                continue

            # Знаходимо існуючий запис у базі або створюємо новий
            material, created = StudyMaterial.objects.get_or_create(
                title=title,
                defaults={
                    'price': price,
                    'is_free': bool(is_free),
                    'is_bundle': bool(is_bundle),
                    'is_published': True
                }
            )

            # Оновлюємо дані (якщо ви, наприклад, змінили ціну в таблиці)
            material.price = price
            material.is_free = bool(is_free)
            material.is_bundle = bool(is_bundle)
            material.is_published = True

            self.stdout.write(f"Зшиваю та завантажую в Cloudinary: {title} ...")

            # ПРИМУСОВО додаємо PDF (це викличе склеювання з intro.pdf)
            with open(pdf_path, 'rb') as f:
                material.file.save(filename, File(f), save=True)

            self.stdout.write(self.style.SUCCESS(f'Успішно оновлено: {title}'))

        self.stdout.write(self.style.SUCCESS('Усі матеріали успішно завантажено в базу та на Cloudinary!'))