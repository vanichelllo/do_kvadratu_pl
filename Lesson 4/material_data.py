# material_data.py

# 1. Декларація текстових змінних (Тип: str)
# Зберігаємо метадані навчального конспекту для підготовки до іспиту
material_title = "Комплексний аналіз параметрів. Частина 1"
file_storage_path = "/media/protected/pdfs/algebra_params_v1.pdf"
brand_identifier = "do_kvadratu"

# 2. Декларація числових змінних (Типи: int та float)
# Базова вартість продукту в гривнях та розмір файлу на сервері
base_price = 450
file_size_mb = 12.85

# 3. Декларація логічної змінної (Тип: bool)
# Прапорець, який керує видимістю матеріалу на сайті для покупців
is_published = True

# 4. Аналітичні обчислення (Імітація бізнес-логіки)
# Розраховуємо акційну ціну зі знижкою 20% для перших міні-груп
discount_rate = 0.20
discount_amount = base_price * discount_rate
final_price = base_price - discount_amount

# 5. Інспекція об'єктів у пам'яті комп'ютера
# Використовуємо вбудовані функції type() для перевірки типів
# та id() для перегляду унікальних адрес об'єктів у пам'яті
print("=== СИСТЕМНИЙ АНАЛІЗ ОБ'ЄКТІВ ПАМ'ЯТІ ===")
print("Назва типу для material_title:", type(material_title), "| ID у пам'яті:", id(material_title))
print("Назва типу для base_price:", type(base_price), "| ID у пам'яті:", id(base_price))
print("Назва типу для file_size_mb:", type(file_size_mb), "| ID у пам'яті:", id(file_size_mb))
print("Назва типу для is_published:", type(is_published), "| ID у пам'яті:", id(is_published))
print("Назва типу для final_price:", type(final_price), "| ID у пам'яті:", id(final_price))

# 6. Форматування виводу даних через f-рядки (Formatted string literals)
# f-рядки дозволяють безпосередньо інтегрувати змінні та обчислення всередину тексту.
# Це стандарт сучасного Python для генерації логів сервера та динамічних HTML-сторінок.
print("\n=== КАРТКА НАВЧАЛЬНОГО МАТЕРІАЛУ ДЛЯ КЛІЄНТА ===")

# Створюємо структурований вивід метаданих продукту
catalog_card = f"""Бренд: {brand_identifier}
Назва продукту: {material_title}
Шлях до захищеного файлу: {file_storage_path}
Розмір файлу для завантаження: {file_size_mb} MB
Статус публікації на платформі: {is_published}
Початкова вартість: {base_price} UAH
Діюча знижка: {discount_rate * 100}%
Фінальна ціна для міні-груп: {final_price} UAH"""

print(catalog_card)