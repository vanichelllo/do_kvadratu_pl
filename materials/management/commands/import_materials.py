import os
from django.core.management.base import BaseCommand
from django.core.files import File
from openpyxl import load_workbook
from materials.models import StudyMaterial, Category


class Command(BaseCommand):
    help = 'Додає нові матеріали з matrix.xlsx (наявні не змінює). Запускається на Render при кожному деплої.'

    def handle(self, *args, **kwargs):
        excel_path = 'matrix.xlsx'
        pdf_folder = 'import_files'

        category, _ = Category.objects.get_or_create(name="Підготовка до НМТ")

        wb = load_workbook(excel_path)
        ws = wb.active

        self.stdout.write("Шукаємо нові матеріали в matrix.xlsx...")
        created_count = 0

        for row in ws.iter_rows(min_row=2, values_only=True):
            excel_title, original_price, filename, is_free, is_bundle = row[:5]

            if not excel_title or not filename:
                continue

            new_title = excel_title
            price = 25  # Нові окремі теми — по 25 грн

            if is_bundle:
                price = original_price  # Пакети — з ціною з Excel
                if "Пакет 1" in excel_title:
                    new_title = "Вся алгебра для НМТ"
                elif "Пакет 2" in excel_title:
                    new_title = "Вся геометрія для НМТ"
                elif "Пакет 3" in excel_title:
                    new_title = "Весь курс для НМТ"

            # Наявні матеріали НЕ змінюємо: ціну, видимість, назву й файл ви керуєте в адмінці,
            # і деплой більше не повертає їх до значень з Excel
            if StudyMaterial.objects.filter(title__in=[excel_title, new_title]).exists():
                continue

            material = StudyMaterial.objects.create(
                title=new_title,
                price=price or 0,
                is_free=bool(is_free),
                is_bundle=bool(is_bundle),
                is_published=True,
                category=category,
            )
            created_count += 1

            pdf_path = os.path.join(pdf_folder, filename)
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    material.file.save(filename, File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f'Створено з PDF: {new_title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Створено без PDF (файл {filename} не знайдено): {new_title}'))

        self.stdout.write(self.style.SUCCESS(f'Готово! Нових матеріалів: {created_count}. Наявні не змінювались.'))
