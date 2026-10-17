"""Конспекти й індивідуальні уроки, збережені в базі, підключали MathJax як mathjax@3 — будь-яку нову 3.x з CDN.
Закріплюємо ту саму версію, що й у шаблонах сайту, щоб оновлення на CDN не зламало формули в усіх уроках одразу."""
from django.db import migrations
from django.db.models import Value
from django.db.models.functions import Replace

OLD, NEW = 'npm/mathjax@3/', 'npm/mathjax@3.2.2/'


def forwards(apps, schema_editor):
    for model_name in ('StudyMaterial', 'StudentPresentation'):
        model = apps.get_model('materials', model_name)
        model.objects.filter(html_content__contains=OLD).update(
            html_content=Replace('html_content', Value(OLD), Value(NEW)))


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0038_game_mistake'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
