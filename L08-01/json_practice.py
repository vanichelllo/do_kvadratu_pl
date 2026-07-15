import json

student_db = {
    "name": "Олена",
    "balance": 50,
    "purchased_courses": ["Вектори", "Параметри"]
}

with open("database.json", "w", encoding="utf-8") as file:
    json.dump(student_db, file, ensure_ascii = False, indent = 4)
    print("Дані успішно збережено у файл database.json!")

with open("database.json", "r", encoding="utf-8") as file:
    restored_student = json.load(file)
    print(f"""Баланс відновленого учня - {restored_student['balance']}.
Перший куплений курс відновленого учня - {restored_student['purchased_courses'][0]}""")