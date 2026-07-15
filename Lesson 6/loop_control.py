# loop_control.py

# Симуляція даних групи
cohort_students = [
    {"student_id": 101, "email": "rinat@test.com", "status": "active"},
    {"student_id": 102, "email": "andriy@test.com", "status": "banned"},
    {"student_id": 103, "email": "davyd@test.com", "status": "active"},
    {"student_id": 104, "email": "melissa@test.com", "status": "active"}
]

print("=== СЦЕНАРІЙ 1: ВИКОРИСТАННЯ CONTINUE (ФІЛЬТРАЦІЯ) ===")
# Завдання: розіслати PDF усім, окрім заблокованих

for student in cohort_students:
    if student["status"] == "banned":
        print(f"[Skipped] Учень {student['email']} заблокований. Пропускаємо.")
        # Оператор continue миттєво повертає нас на початок циклу for.
        # Рядки коду нижче (для цього конкретного учня) виконані НЕ будуть.
        continue

    # Цей код виконається ТІЛЬКИ для тих, хто НЕ "banned"
    print(f"[Success] Відправка PDF на email: {student['email']}")

print("\n=== СЦЕНАРІЙ 2: ВИКОРИСТАННЯ BREAK (ПОШУК) ===")
# Завдання: знайти учня з ID 103 і зупинити пошук

target_id = 103
found_student_email = None  # Тимчасова порожня змінна для збереження результату

for student in cohort_students:
    print(f"Аналізуємо ID {student['student_id']}...")

    if student["student_id"] == target_id:
        found_student_email = student["email"]
        print(">> Учня знайдено! Зупиняємо пошук бази даних.")
        # Оператор break миттєво "вбиває" цикл. Мелісу (ID 104) ми навіть не будемо перевіряти.
        break

# Цей код виконається після завершення (або переривання) циклу
print(f"Результат пошуку: {found_student_email}") 