base_price = 1500.0
nmt_mock_score = 185
if nmt_mock_score >= 190:
    final_price = base_price * 0.8
    print(f"Грант 20%! Ваша ціна: {final_price} UAH.")
elif nmt_mock_score >= 170:
    final_price = base_price * 0.9
    print(f"Грант 10%! Ваша ціна: {final_price} UAH.")
else:
    print(f"Стандартна вартість. Ваша ціна: {base_price} UAH.")

is_banned = False                  # Статус блокування профілю
student_cohort = "Група-А"         # До якої групи належить учень
material_cohort = "Група-А"        # Для якої групи призначений PDF-файл
access_days_left = 0               # Кількість днів до закінчення доступу

if is_banned:
    print("Критична помилка: Акаунт заблоковано")
else:
    if student_cohort == material_cohort:
        if access_days_left > 0:
            print("Доступ надано. Завантаження файлу...")
        else:
            print("Помилка: Ваш період доступу до матеріалів цієї групи завершився.")
    else:
        print("Помилка: Цей матеріал призначений для іншої міні-групи.")