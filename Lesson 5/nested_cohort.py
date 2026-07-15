# nested_cohort.py

# 1. Створюємо список, всередині якого знаходяться словники
# Кожен словник описує окремого учня
nmt_group_a = [
    {
        "student_id": 101,
        "first_name": "Андрій",
        "email": "andriy@example.com",
        "has_paid": True
    },
    {
        "student_id": 102,
        "first_name": "Давид",
        "email": "davyd@example.com",
        "has_paid": False
    },
    {
        "student_id": 103,
        "first_name": "Мелісса",
        "email": "melissa@example.com",
        "has_paid": True
    }
]

print("=== ЗАГАЛЬНА СТАТИСТИКА ГРУПИ ===")
print(f"Кількість зареєстрованих учнів: {len(nmt_group_a)}")

# 2. Ланцюговий доступ до даних (Chained Access)
# Достаємо ім'я першого учня (індекс 0, ключ 'first_name')
first_student_name = nmt_group_a[0]["first_name"]

# Достаємо статус оплати другого учня (індекс 1, ключ 'has_paid')
second_student_payment = nmt_group_a[1]["has_paid"]

print("\n=== ТОЧКОВИЙ ДОСТУП ДО ДАНИХ ===")
print(f"Перший учень у списку: {first_student_name}")
print(f"Статус оплати учня Давид: {second_student_payment}")

# 3. Модифікація вкладених даних
# Припустимо, Давид (індекс 1) здійснив оплату. Оновлюємо його статус:
nmt_group_a[1]["has_paid"] = True

print("\n=== ПІСЛЯ ОНОВЛЕННЯ ОПЛАТИ ===")
print(f"Новий статус оплати учня Давид: {nmt_group_a[1]['has_paid']}")

# 4. Додавання нового словника до існуючого списку
# Створюємо словник для нового учня
new_student = {
    "student_id": 104,
    "first_name": "Олексій",
    "email": "oleksiy@example.com",
    "has_paid": True
}

# Додаємо його в кінець списку групи
nmt_group_a.append(new_student)

print("\n=== ПІСЛЯ ДОДАВАННЯ НОВОГО УЧНЯ ===")
print(f"Тепер у групі {len(nmt_group_a)} учні(в).")
# Перевіряємо дані останнього доданого учня (індекс -1)
print(f"Останній зарахований учень: {nmt_group_a[-1]['first_name']}")