# payment_reminder.py

# 1. Наша база даних (список словників)
cohort_students = [
    {"name": "Рінат", "has_paid": True, "email": "rinat@example.com"},
    {"name": "Андрій", "has_paid": False, "email": "andriy@example.com"},
    {"name": "Давид", "has_paid": True, "email": "davyd@example.com"},
    {"name": "Мелісса", "has_paid": False, "email": "melissa@example.com"}
]

print("=== ЗАПУСК СИСТЕМИ АВТОМАТИЧНИХ НАГАДУВАНЬ ===")

# 2. Оголошуємо змінну-лічильник для аналітики перед циклом
reminders_sent = 0

# 3. Запускаємо цикл for
# Змінна 'student' на кожній ітерації буде містити словник одного конкретного учня
for student in cohort_students:

    # Тіло циклу (відступ 4 пробіли)
    # Звертаємося до словника поточного учня через ланцюговий доступ
    if student["has_paid"] == False:  # Або більш професійно: if not student["has_paid"]:

        # Відступ 8 пробілів (вкладеність if всередині for)
        print(f"Відправка email на {student['email']}...")
        print(f"Повідомлення: Шановний(а) {student['name']}, нагадуємо про необхідність оплати курсу.")
        print("-" * 30)  # Візуальний розділювач

        # Збільшуємо лічильник відправлених повідомлень на 1
        reminders_sent = reminders_sent + 1

# Цей код знаходиться поза циклом і виконається лише після його повного завершення
print("=== РОБОТУ ЗАВЕРШЕНО ===")
print(f"Загалом відправлено нагадувань: {reminders_sent}")