def init_cohort(cohort_name, subject="Математика", max_students=4):
    print(f"""[Система]
    Створено групу: {cohort_name}.
    Предмет: {subject}.
    Ліміт місць: {max_students}.""")


init_cohort("НМТ-2027-Альфа")
init_cohort("IT-Математика", "Математика", 6)


def calculate_fop_revenue(students_qty, price_per_student, tax_rate=0.05):
    gross_revenue = students_qty * price_per_student
    tax_amount = gross_revenue * tax_rate
    net_revenue = gross_revenue - tax_amount
    print(f"""Чистий дохід з групи: {net_revenue} UAH (Податок: {tax_amount} UAH).""")


calculate_fop_revenue(4, 1500)


def generate_student_profiles(names_list, target_cohort):
    database = []
    for name in names_list:
        dict_student = {"name": name, "cohort": target_cohort, "is_active": True}
        database.append(dict_student)
    print(database)


generate_student_profiles(["Рінат", "Олексій"], "НМТ-Інтенсив")
