# cohort_data_structures.py

# 1. Створюємо окремі словники для кожного учня.
# Ключами є рядки (назви колонок), а значеннями - різні типи даних (str, bool).
student_1 = {
    "first_name": "Рінат",
    "email": "rinat@example.com",
    "is_active": True
}

student_2 = {
    "first_name": "Андрій",
    "email": "andriy@example.com",
    "is_active": True
}

student_3 = {
    "first_name": "Давид",
    "email": "davyd@example.com",
    "is_active": False  # Наприклад, учень призупинив навчання
}

student_4 = {
    "first_name": "Мелісса",
    "email": "melissa@example.com",
    "is_active": True
}

# 2. Створюємо список (List), який об'єднує цих учнів у міні-групу.
# Квадратні дужки [] позначають створення списку.
nmt_cohort_2027 = [student_1, student_2, student_3, student_4]

# 3. Демонстрація доступу до даних

# Виводимо загальну кількість учнів у групі за допомогою вбудованої функції len()
print(f"Загальна кількість учнів у міні-групі: {len(nmt_cohort_2027)}")

# Доступ до конкретного учня за індексом.
# Оскільки індексація починається з 0, індекс [0] поверне першого учня (Ріната).
first_student_in_list = nmt_cohort_2027[0]
print("\n--- Дані першого учня ---")
print(first_student_in_list)

# Ланцюговий доступ: спочатку беремо словник зі списку за індексом [1] (Андрій),
# а потім зі словника беремо значення за ключем ["email"].
second_student_email = nmt_cohort_2027[1]["email"]
print("\n--- Точковий запит даних ---")
print(f"Електронна пошта другого учня у списку: {second_student_email}")

# 4. Модифікація структур даних у рантаймі

# Змінюємо статус активності Давида (індекс 2) на True
nmt_cohort_2027[2]["is_active"] = True
print(f"\nСтатус учня {nmt_cohort_2027[2]['first_name']} оновлено на: {nmt_cohort_2027[2]['is_active']}")

# Додаємо нового учня у список за допомогою методу списків .append()
student_5 = {
    "first_name": "Олексій",
    "email": "oleksiy@example.com",
    "is_active": True
}
nmt_cohort_2027.append(student_5)

print(f"\nНова кількість учнів після додавання: {len(nmt_cohort_2027)}")

student_6 = {
    "first_name": "Давид",
    "email":"davyd@gmail.com",
    "is_active": True
}
nmt_cohort_2027.append(student_6)

message = f"""\nНовий учень {nmt_cohort_2027[5]['first_name']} успішно доданий до групи. Контактний email: {nmt_cohort_2027[5]['email']}."""
print(message)