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
nmt_group_a[2]["email"] = "melissa.new@gmail.com"
new_student = {
    "student_id": 104,
    "first_name": "Рінат",
    "email": "rinat@example.com",
    "has_paid": False}
nmt_group_a.insert(0, new_student)
print(f"""Оновлення бази. Перший учень у групі тепер: {nmt_group_a[0]["first_name"]}.
Email Мелісси оновлено на: {nmt_group_a[3]["email"]}.
Загальна кількість: {len(nmt_group_a)}.""")