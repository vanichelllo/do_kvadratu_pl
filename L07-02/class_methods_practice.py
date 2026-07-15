class NMTMaterial:
    def __init__(self,title,price):
        self.title = title
        self.price = price

    def calculate_grant_price(self, discount_percent):
        promo_price = self.price * (1 - discount_percent)
        return promo_price
topic = NMTMaterial("Параметр",600.0)
print(topic.calculate_grant_price(0.15))

class MiniGroup:
    def __init__(self,name,max_capacity):
        self.name = name
        self.max_capacity = max_capacity
        self.students = []
    def enroll_student(self,student_name):
        if len(self.students) <= self.max_capacity:
            self.students.append(student_name)
            print(self.students)
            print(f"[Успіх] {student_name} додано до групи {self.name}")
        else:
            print(f"[Відмова] Група {self.name} повністю заповнена. {student_name} переведено в резерв.")
gr = MiniGroup("1",2)
gr.enroll_student("Дар'я")
gr.enroll_student("Дар'я")
gr.enroll_student("Дар'я")