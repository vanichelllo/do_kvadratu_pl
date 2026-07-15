# material_builder.py

# 1. Оголошення функції
# title та base_price - обов'язкові позиційні аргументи
# discount та is_published - необов'язкові іменовані аргументи зі значеннями за замовчуванням
def create_material_card(title, base_price, discount=0.0, is_published=False):
    # Розраховуємо вартість з урахуванням знижки (коефіцієнт від 0.0 до 1.0)
    calculated_price = base_price * (1 - discount)

    # Формуємо стандартизовану структуру словника для бази даних
    material_data = {
        "title": title,
        "base_price": base_price,
        "discount_percent": discount,
        "final_price": calculated_price,
        "is_published": is_published
    }

    # Виводимо технічний лог у консоль
    print(f"[Системний лог] Створено картку об'єкта: {material_data['title']}")
    print(f"Ціна до сплати: {material_data['final_price']} UAH.")
    print("-" * 40)


print("=== ТЕСТУВАННЯ РОБОТИ ФУНКЦІЇ ===")

# Виклик 1: Передаємо тільки обов'язкові позиційні аргументи.
# "Тригонометрія" запишеться в title, 500.0 - в base_price.
# discount автоматично стане 0.0, а is_published - False.
create_material_card("НМТ Спецкурс: Тригонометрія", 500.0)

# Виклик 2: Передаємо всі аргументи як позиційні (суворо за порядком оголошення)
# title="Геометрія", base_price=400.0, discount=0.15 (15%), is_published=True
create_material_card("Планіметрія. Трикутники", 400.0, 0.15, True)

# Виклик 3: Використовуємо іменовані аргументи
# Завдяки вказуванню імен ми можемо міняти їх місцями або пропускати деякі з них.
# Python чітко знає, куди записати True, а куди 0.20
create_material_card(
    is_published=True,
    base_price=600.0,
    discount=0.20,
    title="Повний курс: Комбінаторика"
)