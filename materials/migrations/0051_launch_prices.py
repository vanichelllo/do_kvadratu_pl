from django.db import migrations

NMT_SUBJECT_NAME = "Підготовка до НМТ / ЗНО"

# Ціни тарифів викладача (місяць, навчальний рік), погоджені власником 19.10.2026
TUTOR_PRICES = {'Старт': (249, 1790), 'Профі': (449, 3290), 'Безліміт': (749, 5490), 'НМТ': (149, 990)}


def launch(apps, schema_editor):
    """Рішення власника 19.10.2026:
    1) підписка на 5 клас продається з позначкою раннього доступу;
    2) тарифи викладача, яким ще не ставили ціни, отримують погоджені ціни й вмикаються (ціни, задані в адмінці,
       не змінюються);
    3) шкільні уроки, завантажені з репозиторію до автопублікації й досі неопубліковані, публікуються."""
    ClassPlan = apps.get_model('materials', 'ClassPlan')
    TeacherPlan = apps.get_model('materials', 'TeacherPlan')
    StudyMaterial = apps.get_model('materials', 'StudyMaterial')

    plan = ClassPlan.objects.filter(number=5).first()
    if plan:
        plan.is_active = True
        plan.note = plan.note or 'Ранній доступ: нові уроки щотижня'
        plan.save(update_fields=['is_active', 'note'])

    for name, (month, year) in TUTOR_PRICES.items():
        TeacherPlan.objects.filter(name=name, price_month=0, price_year=0).update(
            price_month=month, price_year=year, is_active=True)

    (StudyMaterial.objects.filter(is_published=False, is_bundle=False, curriculum_topic__isnull=False)
     .exclude(html_source_hash='')
     .exclude(curriculum_topic__chapter__grade__subject__name=NMT_SUBJECT_NAME)
     .update(is_published=True))


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0050_class_subscriptions"),
    ]

    operations = [
        migrations.RunPython(launch, migrations.RunPython.noop),
    ]
