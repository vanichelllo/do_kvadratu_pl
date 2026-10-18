from django.db import migrations


def create_special_topics(apps, schema_editor):
    """Узагальнення кожного розділу й діагностика кожного класу для вже завантаженого класифікатора."""
    from materials.curriculum import ensure_special_topics
    ensure_special_topics(apps.get_model('materials', 'CurriculumGrade'), apps.get_model('materials', 'CurriculumChapter'),
                          apps.get_model('materials', 'CurriculumTopic'), apps.get_model('materials', 'StudyMaterial'))


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0041_school_practice"),
    ]

    operations = [
        migrations.RunPython(create_special_topics, migrations.RunPython.noop),
    ]
