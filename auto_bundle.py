import os
import re
from pypdf import PdfWriter  # <--- ЗМІНЕНО ОСЬ ТУТ


def create_bundles(folder_path=r"C:\Users\iskly\PycharmProjects\do_kvadratu_platform\import_files"):
    # Створюємо три окремі "збирачі" для наших пакетів (тепер використовуємо PdfWriter)
    merger_algebra = PdfWriter()
    merger_geometry = PdfWriter()
    merger_all = PdfWriter()

    # Отримуємо список усіх PDF-файлів у папці
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    # Функція для витягування номера з назви файлу
    def get_file_number(filename):
        match = re.match(r'^(\d+)', filename)
        if match:
            return int(match.group(1))
        return 99999  # Якщо файл без номера, відправляємо його в кінець

    # Сортуємо файли за їхнім номером
    sorted_files = sorted(all_files, key=get_file_number)

    print(f"Знайдено {len(sorted_files)} PDF-файлів. Починаємо сортування...\n")

    added_algebra = 0
    added_geometry = 0
    added_all = 0

    # Проходимося по кожному відсортованому файлу
    for filename in sorted_files:
        file_path = os.path.join(folder_path, filename)
        file_number = get_file_number(filename)

        # Пропускаємо файли без номерів (або вже згенеровані пакети)
        if file_number == 99999:
            continue

        # 1. Додаємо УСІ файли в загальний пакет
        merger_all.append(file_path)
        added_all += 1

        # 2. Якщо номер 29 або менше — це Алгебра
        if file_number <= 29:
            merger_algebra.append(file_path)
            added_algebra += 1
            print(f"[Алгебра] Додано: {filename}")

        # 3. Якщо номер 30 або більше — це Геометрія
        elif file_number >= 30:
            merger_geometry.append(file_path)
            added_geometry += 1
            print(f"[Геометрія] Додано: {filename}")

    # Зберігаємо готові файли
    print("\nЗберігаємо файли...")

    if added_algebra > 0:
        merger_algebra.write("Bundle_01_Algebra.pdf")
        print(f"✅ Пакет 'Алгебра' створено (включено файлів: {added_algebra})")

    if added_geometry > 0:
        merger_geometry.write("Bundle_02_Geometria.pdf")
        print(f"✅ Пакет 'Геометрія' створено (включено файлів: {added_geometry})")

    if added_all > 0:
        merger_all.write("Bundle_03_Povnyi_Kurs.pdf")
        print(f"✅ Пакет 'Повний курс' створено (включено файлів: {added_all})")

    # Закриваємо потоки
    merger_algebra.close()
    merger_geometry.close()
    merger_all.close()


if __name__ == "__main__":
    # Викликаємо функцію (вона автоматично візьме шлях, який ви вказали зверху)
    create_bundles()