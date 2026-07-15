# return_logic.py

# 1. Функція, яка розраховує знижку, але НЕ друкує її.
# Вона ПОВЕРТАЄ значення за допомогою ключового слова return.
def calculate_discounted_price(base_price, discount_percent):
    final_price = base_price * (1 - discount_percent)
    return final_price
    # Увага: будь-який код, написаний після return у цьому блоці, ніколи не виконається.

# 2. Викликаємо функцію.
# Оскільки вона має return, ми можемо "зловити" її результат у нову змінну.
premium_cohort_price = calculate_discounted_price(1500.0, 0.20)

# 3. Тепер ми можемо використовувати цю змінну для подальшої бізнес-логіки.
# Наприклад, розрахувати комісію платіжної системи (2.5%).
payment_fee = premium_cohort_price * 0.025

print("=== ФІНАНСОВИЙ ЗВІТ ===")
print(f"Вартість курсу зі знижкою: {premium_cohort_price} UAH")
print(f"Комісія банку: {payment_fee} UAH")

def calculate_ltv(monthly_payment, month_active):
    monthly_sum = monthly_payment * month_active
    return monthly_sum
student_ltv = calculate_ltv(1200.0,5)
promo_student_ltv = student_ltv * 0.15
print(promo_student_ltv)

def has_active_subscription(access_days_left):
    if access_days_left > 0:
        return True
    else:
        return False
access_granted = has_active_subscription(0)
print(access_granted)

exam_results = [
    {"name": "Олексій", "score": 185},
    {"name": "Рінат", "score": 192},
    {"name": "Андрій", "score": 150}
]
def filter_successful_students(students_list):
    successful_students = []
    for student in students_list:
        if student["score"] >= 180:
            successful_students.append(student["name"])
        else:
            continue
    return successful_students
top_students = filter_successful_students(exam_results)
print(top_students)