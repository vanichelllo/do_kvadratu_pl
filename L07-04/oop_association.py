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


class StudyProfile:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.purchased_materials = []
    def __str__(self):
        if self.balance < 0:
            st = f"Учень: {self.name} (БОРГ: {self.balance} UAH"
        else:
            st = f"Учень: {self.name} (Оплачено: {self.balance} UAH"
        return st
    def buy_material(self, material):
        if self.balance >= material.price:
            self.balance -= material.price
            self.purchased_materials.append(material)
            pst = f"[Успіх] {self.name} придбав {material.title}. Залишок: {self.balance}"
        else:
            pst = f"[Відмова] Недостатньо коштів для купівлі {material.title}"
        return pst
m1 = StudyMaterial("Вектори", 250, True)
s1 = StudyProfile("Олена", 300)
result = s1.buy_material(m1)
print(result)

print(s1.purchased_materials[0])