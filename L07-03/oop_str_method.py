# oop_str_method.py

class Cohort:
    def __init__(self, name, max_students):
        self.name = name
        self.max_students = max_students
        self.students = []

    def enroll(self, student_name):
        if len(self.students) < self.max_students:
            self.students.append(student_name)

    # Додаємо магічний метод для читабельного відображення
    def __str__(self):
        # Використовуємо f-рядок для форматування.
        # Обов'язково повертаємо результат через return!
        current_occupancy = len(self.students)
        return f"Група: {self.name} | Заповненість: {current_occupancy}/{self.max_students}"

print("=== ТЕСТУВАННЯ МЕТОДУ __str__ ===")

# Створюємо об'єкт
nmt_math = Cohort("НМТ-2027 Математика", 4)
nmt_math.enroll("Олексій")
nmt_math.enroll("Давид")

# Тепер, коли ми друкуємо сам об'єкт, Python автоматично шукає метод __str__
# і виводить те, що цей метод повернув.
print(nmt_math)

class StudyMaterial:
    def __init__(self, title, price, is_published):
        self.title = title
        self.price = price
        self.is_published = is_published
    def __str__(self):
        if self.is_published == True:
            st = "Опубліковано"
        else:
            st = "Чернетка"
        return f"{st} {self.title} - {self.price} UAH"
m1 = StudyMaterial("Числові множини", 300, True)
m2 = StudyMaterial("Пропорції", 300, False)
print(f"""{m1}
{m2}""")

class StudyProfile:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
    def __str__(self):
        if self.balance < 0:
            st = f"Учень: {self.name} (БОРГ: {self.balance} UAH"
        else:
            st = f"Учень: {self.name} (Оплачено: {self.balance} UAH"
        return st
m1 = StudyProfile("Андрій", -300)
m2 = StudyProfile("Діма", 300)
print(f"""{m1}
{m2}""")