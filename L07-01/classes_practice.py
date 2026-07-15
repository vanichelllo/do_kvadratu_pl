class Material:
    def __init__(self,title,price):
        self.title = title
        self.price = price
        self.is_published = False
math_book = Material("Алгебра",300.0)
print(f"Назва: {math_book.title}. Статус: {math_book.is_published}")
# 1. Оголошення класу (з великої літери)
class Cohort:
    def __init__(self, cohort_name):
        # Зберігаємо передану назву
        self.name = cohort_name
        # Створюємо порожній список для майбутніх учнів
        self.students_list = []

# --- ТУТ КЛАС (КРЕСЛЕННЯ) ЗАКІНЧУЄТЬСЯ. ВІДСТУПІВ БІЛЬШЕ НЕМАЄ ---

# 2. Створення екземпляра (будуємо реальну групу)
nmt_group = Cohort("НМТ-Альфа")

# 3. Взаємодія з об'єктом
# Ми беремо нашу створену групу (nmt_group),
# ставимо крапку, щоб дістати її внутрішній список (students_list),
# і викликаємо метод списку .append()
nmt_group.students_list.append("Іван")
nmt_group.students_list.append("Марія")

# 4. Перевірка
print(nmt_group.students_list)

class PremiumCourse:
    def __init__(self,title,base_price):
        if base_price < 0:
            print("Помилка: ціна не може бути від'ємною!")
            self.price = 0.0
        else:
            self.price = base_price
cs1 = PremiumCourse("1",1500.0)
cs2 = PremiumCourse("2",-500.0)
print(cs1.price)
print(cs2.price)
