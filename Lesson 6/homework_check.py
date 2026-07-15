homework_results = [
    {"name": "Рінат", "score": 95},
    {"name": "Андрій", "score": 60},
    {"name": "Давид", "score": 88},
    {"name": "Мелісса", "score": 72},
    {"name": "Олексій", "score": 45}
]
amount_good_results = 0
amount_bad_results = 0
for student in homework_results:
    if student["score"] >= 70:
        print(f"Учень {student['name']} здав завдання добре (Бал: {student['score']}).")
        amount_good_results += 1
    else:
        print(f"Учню {student['name']} потрібно перескласти матеріал (Бал: {student['score']}).")
        amount_bad_results += 1
print(f"""Кількість тих хто здав: {amount_good_results}
Кількість тих хто не здав: {amount_bad_results}""")