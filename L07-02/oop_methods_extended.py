class NMTStudent:
    def __init__(self, name, target_score):
        self.name = name
        self.target_score = target_score
        self.lessons_attended = 0  # Лічильник відвіданих занять

    # Метод приймає тільки self. Він працює виключно з внутрішніми даними.
    def attend_lesson(self,a):
        self.lessons_attended += a
        print(f"[{self.name}] відвідав заняття. Всього відвідано: {self.lessons_attended}")

    # Метод з логікою (if/else), який повертає результат через return
    def get_readiness_status(self):
        if self.lessons_attended >= 10:
            return "Висока готовність до тесту"
        else:
            return "Потребує більше практики"

print("=== ПРИКЛАД 1: Студенти ===")
student_rinat = NMTStudent("Рінат", 190)
student_andriy = NMTStudent("Андрій", 170)

# Рінат відвідує два заняття. Ми не змінюємо лічильник напряму, метод робить це сам.
student_rinat.attend_lesson(12)
student_rinat.attend_lesson(2)

print(f"Статус Ріната: {student_rinat.get_readiness_status()}")
print(f"Статус Андрія: {student_andriy.get_readiness_status()}")


class EducationalMaterial:
    def __init__(self, title, base_price):
        self.title = title
        self.price = base_price
        self.purchases = 0

    def buy(self):
        self.purchases += 1

    # Метод приймає зовнішній аргумент promo_code_discount
    def calculate_final_price(self, promo_code_discount):
        discount_amount = self.price * promo_code_discount
        return self.price - discount_amount

    def get_total_revenue(self):
        # Метод використовує внутрішні атрибути для фінансового звіту
        return self.purchases * self.price


print("\n=== ПРИКЛАД 2: Матеріали ===")
planimetry_pdf = EducationalMaterial("Планіметрія: Властивості фігур", 400.0)

# Відбулося три покупки
planimetry_pdf.buy()
planimetry_pdf.buy()
planimetry_pdf.buy()

# Розраховуємо ціну з 20% знижкою для конкретного запиту
promo_price = planimetry_pdf.calculate_final_price(0.20)
print(f"Звичайна ціна: {planimetry_pdf.price} UAH. За промокодом: {promo_price} UAH")
print(f"Загальний дохід з матеріалу: {planimetry_pdf.get_total_revenue()} UAH")

class CourseAccess:
    def __init__(self, course_name):
        self.course_name = course_name
        self.allowed_emails = []  # Список дозволених email-адрес (Білий список)

    def grant_access(self, student_email):
        self.allowed_emails.append(student_email)
        print(f"Доступ до '{self.course_name}' надано для {student_email}")

    def check_access(self, email_to_check):
        # Оператор 'in' перевіряє, чи існує елемент у списку
        if email_to_check in self.allowed_emails:
            return True
        else:
            return False

print("\n=== ПРИКЛАД 3: Права доступу ===")
algebra_course = CourseAccess("Алгебра: Спецкурс")

# Надаємо доступ лише одному учню
algebra_course.grant_access("melissa@example.com")

# Перевіряємо права під час спроби завантажити файл
email_request_1 = "melissa@example.com"
email_request_2 = "oleksiy@example.com"

print(f"Доступ для {email_request_1}: {algebra_course.check_access(email_request_1)}")
print(f"Доступ для {email_request_2}: {algebra_course.check_access(email_request_2)}")