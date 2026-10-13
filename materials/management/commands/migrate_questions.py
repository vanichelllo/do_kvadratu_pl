import re
from django.core.management.base import BaseCommand
from django.db import transaction
from materials.models import Question, CurriculumTopic


class Command(BaseCommand):
    help = 'Переносить запитання зі старих DiagnosticTopic у нові CurriculumTopic'

    def handle(self, *args, **kwargs):
        self.stdout.write("Починаємо перенесення завдань...")

        # Беремо всі нові теми з курсу "Підготовка до НМТ / ЗНО"
        nmt_topics = list(CurriculumTopic.objects.filter(chapter__grade__subject__name="Підготовка до НМТ / ЗНО"))

        questions = Question.objects.exclude(topic__isnull=True)
        migrated_count = 0
        error_count = 0

        with transaction.atomic():
            for q in questions:
                # Шукаємо номер у старій назві теми
                match = re.match(r'^(\d+)', q.topic.name)
                if match:
                    topic_num = int(match.group(1))

                    # Шукаємо відповідну нову тему за номером
                    new_topic = None
                    for nt in nmt_topics:
                        nt_match = re.match(r'^(\d+)', nt.name)
                        if nt_match and int(nt_match.group(1)) == topic_num:
                            new_topic = nt
                            break

                    if new_topic:
                        q.curriculum_topic = new_topic
                        q.save(update_fields=['curriculum_topic'])
                        migrated_count += 1
                    else:
                        error_count += 1
                else:
                    error_count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Успішно перенесено завдань: {migrated_count}"))
        if error_count > 0:
            self.stdout.write(self.style.WARNING(f"⚠️ Не вдалося знайти нову тему для {error_count} завдань."))