# advanced_structures.py

# 1. Створення комплексної вкладеної структури даних
# Це імітація відповіді бази даних (JSON) для сторінки "Кабінет міні-групи"
nmt_advanced_cohort = {
    "cohort_id": 101,
    "cohort_name": "НМТ-2027 Інтенсив",
    "start_date": "2026-09-01",
    "tutor_name": "Іван Склянчук",

    # Ключ "students" містить Список Словників
    "students": [
        {
            "first_name": "Рінат",
            "email": "rinat@example.com",
            "scores": [165, 172, 180]  # Вкладений список балів за тести
        },
        {
            "first_name": "Давид",
            "email": "davyd@example.com",
            # Зверніть увагу: у Давида немає ключа "scores" і немає телефону
        }
    ],

    # Ключ "assigned_materials" містить Список Словників
    "assigned_materials": [
        {"title": "Параметри. Частина 1", "is_published": True},
        {"title": "Стереометрія", "is_published": False}
    ]
}

print("=== ДЕМОНСТРАЦІЯ БАГАТОРІВНЕВОГО ДОСТУПУ ===")

# 2. Ланцюговий доступ до глибоко вкладених даних
# Звертаємося до словника -> потім до списку студентів (індекс 0) -> потім до списку балів (індекс 2)
rinat_last_score = nmt_advanced_cohort["students"][0]["scores"][2]
print(f"Останній тестовий бал Ріната: {rinat_last_score}")

print("\n=== БЕЗПЕЧНИЙ ДОСТУП ЧЕРЕЗ .get() ===")

# 3. Використання методу .get() для уникнення KeyError
# Пробуємо отримати телефон Давида (індекс 1). Якщо ключа немає, повертаємо "Не вказано"
davyd_phone = nmt_advanced_cohort["students"][1].get("phone_number", "Номер не вказано в базі")
print(f"Контактний номер Давида: {davyd_phone}")

# Пробуємо отримати бали Давида. Оскільки їх немає, ставимо порожній список [] за замовчуванням
davyd_scores = nmt_advanced_cohort["students"][1].get("scores", [])
print(f"Бали Давида за тестування: {davyd_scores}")

print("\n=== МОДИФІКАЦІЯ СКЛАДНИХ СТРУКТУР ===")

# 4. Додавання нового матеріалу до списку матеріалів когорти
new_material = {"title": "Вектори у просторі", "is_published": True}
nmt_advanced_cohort["assigned_materials"].append(new_material)

print(f"Оновлений список матеріалів групи: {len(nmt_advanced_cohort['assigned_materials'])} шт.")