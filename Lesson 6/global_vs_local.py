# global_vs_local.py

# Глобальна змінна (видно всім)
platform_name = "do_kvadratu"


def process_transaction(amount):
    # Локальна змінна (існує тільки всередині process_transaction)
    bank_fee = amount * 0.02
    net_income = amount - bank_fee

    # Функція може читати глобальні змінні
    print(f"Платформа: {platform_name}")

    return net_income


# Виклик функції
final_amount = process_transaction(1000.0)

# Цей код викличе критичну помилку: NameError: name 'bank_fee' is not defined
# Ми не можемо "побачити" bank_fee ззовні, пам'ять про неї вже знищена.
# print(f"Комісія склала: {bank_fee}")

phones = ["+380671234567", "0509876543", "+380630000000", "test_number"]
def validate_phone_numbers(phones_list):
    correct_phones = []
    for phone in phones_list:
        if phone[:4] == "+380" and len(phone) == 13:
            correct_phones.append(phone)
        else:
            continue
    return correct_phones
final = validate_phone_numbers(phones)
print(final)

# Звичайний невідсортований масив
raw_data = [
    {"name": "A", "val": 10},
    {"name": "B", "val": 50},
    {"name": "C", "val": 30}
]

# Створюємо новий відсортований масив
# Змінна 'item' у лямбда-функції - це просто тимчасова назва для кожного словника під час перевірки
sorted_data = sorted(raw_data, key=lambda item: item["val"], reverse=True)

print("=== ВІДСОРТОВАНИЙ МАСИВ ===")
for element in sorted_data:
    print(element)

new_students = [
    {"name": "Олена", "score": 195},
    {"name": "Тимур", "score": 182},
    {"name": "Марія", "score": 190},
    {"name": "Ігор", "score": 160}
]

def group(new_students_gr,max_group_num):
    sorted_new_students = sorted(new_students_gr,key=lambda new_students_gr: new_students_gr["score"],reverse=True)
    spots_left = max_group_num
    for student in sorted_new_students:
        if student["score"] >= 180 and spots_left > 0:
            student["cohort"] = "НМТ-Альфа"
            spots_left -= 1
        elif student["score"] >= 180:
            student["cohort"] = "Резерв-Альфа"
        else:
            student["cohort"] = "НМТ-База"
    return sorted_new_students
final = group(new_students,2)
print(final)