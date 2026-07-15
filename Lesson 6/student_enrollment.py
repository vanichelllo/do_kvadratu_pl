def register_new_student(full_name,email,cohort_name="Загальна черга", initial_balance=0.0):
    student_card = {
        "full_name":full_name,
        "email":email,
        "cohort_name":cohort_name,
        "initial_balance":initial_balance
    }
    print(student_card)
register_new_student("a","a@a.a")
register_new_student(
    full_name="b",
    email="b@b.b",
    cohort_name="bb",
    initial_balance=1
)