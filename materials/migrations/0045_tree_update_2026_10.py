from django.db import migrations


def update_tree(apps, schema_editor):
    """Доповнення дерева тем: нові теми й перенумерування наявних (див. materials.curriculum.TREE_UPDATE_2026_10)."""
    from materials.curriculum import apply_tree_update, ensure_special_topics
    Grade, Chapter = apps.get_model('materials', 'CurriculumGrade'), apps.get_model('materials', 'CurriculumChapter')
    Topic, Material = apps.get_model('materials', 'CurriculumTopic'), apps.get_model('materials', 'StudyMaterial')
    apply_tree_update(Grade, Chapter, Topic, Material)
    ensure_special_topics(Grade, Chapter, Topic, Material)


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0044_tutor_plans"),
    ]

    operations = [
        migrations.RunPython(update_tree, migrations.RunPython.noop),
    ]
