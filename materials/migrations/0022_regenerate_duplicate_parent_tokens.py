import uuid

from django.db import migrations
from django.db.models import Count


def regenerate_duplicate_parent_tokens(apps, schema_editor):
    """Міграція 0020 видала всім наявним заявкам ОДИН і той самий parent_token
    (default=uuid4 обчислюється один раз на AddField). Даємо кожній власний."""
    TutorStudentRequest = apps.get_model('materials', 'TutorStudentRequest')

    duplicated = (TutorStudentRequest.objects.values('parent_token')
                  .annotate(n=Count('id')).filter(n__gt=1).values_list('parent_token', flat=True))
    to_fix = TutorStudentRequest.objects.filter(parent_token__in=list(duplicated)) | \
        TutorStudentRequest.objects.filter(parent_token__isnull=True)

    for student_request in to_fix:
        student_request.parent_token = uuid.uuid4()
        student_request.save(update_fields=['parent_token'])


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0021_cart_promo_code'),
    ]

    operations = [
        migrations.RunPython(regenerate_duplicate_parent_tokens, migrations.RunPython.noop),
    ]
