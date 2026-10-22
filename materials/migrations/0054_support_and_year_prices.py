from django.db import migrations

# Рішення власника 22.10.2026: річна підписка 5–6 класів — 690 ₴ (старші класи — з тією ж градацією),
# супровід — 449 ₴/міс для класів, що вже продаються. Ціни, змінені в адмінці, не чіпаємо
YEAR_PRICES = {5: (449, 690), 6: (449, 690), 7: (549, 790), 8: (549, 790), 9: (549, 790),
               10: (649, 890), 11: (649, 890)}
SUPPORT_PRICE = 449


def set_prices(apps, schema_editor):
    ClassPlan = apps.get_model('materials', 'ClassPlan')
    for number, (old, new) in YEAR_PRICES.items():
        ClassPlan.objects.filter(number=number, price_year=old).update(price_year=new)
    ClassPlan.objects.filter(is_active=True, support_price_month=0).update(support_price_month=SUPPORT_PRICE)


class Migration(migrations.Migration):
    dependencies = [('materials', '0053_class_support')]
    operations = [migrations.RunPython(set_prices, migrations.RunPython.noop)]
