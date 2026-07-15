# safe_retrieval.py

# Моделюємо неповні дані учня з бази. Зверніть увагу: ключі 'phone' та 'discount' відсутні.
student_db_record = {
    "student_id": 105,
    "first_name": "Іван",
    "email": "ivan.s@example.com",
    "course": "Математика НМТ"
}

print("=== ДЕМОНСТРАЦІЯ БЕЗПЕЧНОГО ЧИТАННЯ ===")

# 1. Пряме звернення до існуючого ключа (працює штатно)
student_email = student_db_record["email"]
print(f"Знайдено email: {student_email}")

# 2. Використання методу .get() для існуючого ключа
# Поверне "Іван", другий аргумент ігнорується, бо ключ "first_name" існує
student_name = student_db_record.get("first_name", "Анонім")
print(f"Знайдено ім'я: {student_name}")

# 3. Використання методу .get() для ВІДСУТНЬОГО ключа
# Ключа "phone" немає, тому система безпечно поверне рядок "Не вказано"
student_phone = student_db_record.get("phone", "Не вказано")
print(f"Телефон користувача: {student_phone}")

# 4. Обчислення з використанням безпечних дефолтних значень
base_price = 1000.0
# Шукаємо знижку. Якщо ключа "discount_percent" немає, вважаємо, що знижка = 0.0
personal_discount = student_db_record.get("discount_percent", 0.0)

# Відсоток переводимо у формат коефіцієнта і рахуємо фінальну ціну
final_price = base_price * (1 - personal_discount)

print("\n=== РОЗРАХУНОК ВАРТОСТІ ===")
print(f"Застосована знижка: {personal_discount * 100}%")
print(f"До сплати: {final_price} UAH")

# Увага: Якщо розкоментувати рядок нижче, програма впаде з помилкою KeyError
# crash_test = student_db_record["phone"]