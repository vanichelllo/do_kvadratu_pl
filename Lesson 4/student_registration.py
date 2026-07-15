student_full_name = "Іван Склянчук"
email = "isklyanchuk5@gmai,.com"
NMT_target_score = 190
advance_payment_sum_group = 700.0
verification = True

new_verification = not(verification)

print("Лог верифікації")

log_verification = f"""Учень: {student_full_name} (type{student_full_name}, id{student_full_name})
Емейл - {email} (type{email}, id{email})
Очікуваний бал = {NMT_target_score} (type{NMT_target_score}, id{NMT_target_score})
Сума = {advance_payment_sum_group} (type{advance_payment_sum_group}, id{advance_payment_sum_group})
Статус верифікації - {new_verification} (type{new_verification}, id{new_verification})"""

print(log_verification)