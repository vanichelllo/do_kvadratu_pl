# student_dict.py

# 1. Ініціалізація словника (використовуються фігурні дужки {})
# Кожен рядок — це пара "ключ": значення
student_profile = {
    "student_id": 1024,
    "full_name": "Рінат Ахметов",
    "email": "rinat.edu@example.com",
    "is_active": True,
    "advance_balance": 1200.0
}

print("=== ВХІДНІ ДАНІ ПРОФІЛЮ ===")
print(student_profile)

# 2. Доступ до значень за допомогою квадратних дужок []
# Передаємо рядок-ключ всередину дужок
current_name = student_profile["full_name"]
current_balance = student_profile["advance_balance"]

print("\n=== ЧИТАННЯ ПАРАМЕТРІВ ===")
print(f"Користувач: {current_name}")
print(f"Поточний баланс на платформі: {current_balance} UAH")

# 3. Модифікація існуючих значень
# Списуємо 450 UAH за купівлю одного PDF-конспекту з параметрів
student_profile["advance_balance"] = current_balance - 450.0

print("\n=== ПІСЛЯ СПИСАННЯ КОШТІВ ===")
print(f"Новий баланс користувача: {student_profile['advance_balance']} UAH")

# 4. Додавання нових пар "ключ-значення" в існуючий словник
# Якщо Python бачить, що такого ключа немає в структурі, він автоматично створює його
student_profile["target_nmt_score"] = 195
student_profile["verification_status"] = True

print("\n=== ОНОВЛЕНА КАРТКА КОРИСТУВАЧА ===")
# Використовуємо f-рядок для структурованого виводу
updated_log = f"""ID Студента: {student_profile['student_id']}
ПІБ: {student_profile['full_name']}
Цільовий бал НМТ: {student_profile['target_nmt_score']}
Статус верифікації: {student_profile['verification_status']}"""

print(updated_log)

material_item = {
    "material.id":1,
    "title":"Числові множини",
    "base_price":200,
    "is_published":False}

material_item["is_published"] = True
material_item["file_size_mb"] = 8.45
print(f"""Системний лог матеріалу ID: {material_item["material.id"]}.
Конспект '{material_item["title"]}' переведено в статус публікації: {material_item["is_published"]}.
Розмір файлу: {material_item["file_size_mb"]} MB.""")
