from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0030_remove_question_topic_remove_studentreport_topic_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curriculumchapter',
            options={'ordering': ['grade__subject__order', 'grade__order', 'order'], 'verbose_name': 'Розділ', 'verbose_name_plural': '3. Розділи'},
        ),
        migrations.AlterModelOptions(
            name='curriculumtopic',
            options={'ordering': ['chapter__grade__subject__order', 'chapter__grade__order', 'chapter__order', 'order'], 'verbose_name': 'Тема', 'verbose_name_plural': '4. Теми (Уроки)'},
        ),
    ]
