# oop_basics.py

# 1. Створення Класу (Креслення)
# Назви класів у Python завжди пишуться з великої літери (CamelCase)
class Student:

    # 2. Конструктор класу
    # Визначаємо, які дані потрібні для створення об'єкта
    def __init__(self, full_name, email, initial_balance=0.0):
        # Присвоюємо передані аргументи у внутрішню пам'ять об'єкта (self)
        self.name = full_name
        self.contact_email = email
        self.balance = initial_balance
        self.is_active = True  # Значення за замовчуванням для всіх нових об'єктів


print("=== СТВОРЕННЯ ОБ'ЄКТІВ ===")

# 3. Створення екземплярів (Об'єктів)
# Ми викликаємо клас за його іменем. Аргумент 'self' передавати НЕ треба,
# Python підставляє його автоматично "під капотом".
student_1 = Student("Олена Іванова", "olena@test.com", 1500.0)
student_2 = Student("Тимур Петров", "timur@test.com")  # balance автоматично стане 0.0

# 4. Взаємодія з об'єктами
# Доступ до даних здійснюється через крапку (dot notation), а не через квадратні дужки
print(f"Учень 1: {student_1.name}. Баланс: {student_1.balance}")
print(f"Учень 2: {student_2.name}. Баланс: {student_2.balance}")

# 5. Зміна стану об'єкта
# Ми можемо безпечно змінювати атрибути конкретного об'єкта
student_2.balance = 500.0
student_1.is_active = False

print("\n=== ПІСЛЯ МОДИФІКАЦІЇ ===")
print(f"Баланс Тимура оновлено: {student_2.balance}")
print(f"Статус Олени (is_active): {student_1.is_active}")