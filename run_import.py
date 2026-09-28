import os
import django

# Налаштування оточення Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'do_kvadratu.settings')
django.setup()

from materials.models import StudyMaterial, Question, AnswerOption, MatchItem, DiagnosticTopic

# ІМПОРТ ДАНИХ З ФАЙЛУ-СХОВИЩА (Для нових тем просто змінюй назву файлу)
from import_files.bank_01 import TOPIC_NAME, TASKS


def run():
    print(f"🔄 Починаємо імпорт завдань...")

    # Знаходимо або створюємо загальну тему (для стартового діагностичного тесту)
    topic, _ = DiagnosticTopic.objects.get_or_create(name=TOPIC_NAME)

    count = 0
    for data in TASKS:
        # 1. Створюємо саме завдання
        q = Question.objects.create(
            topic=topic,
            question_type=data['type'],
            difficulty=data['difficulty'],
            text=data['text'],
            svg_code=data.get('svg_code', '')
        )

        # 2. ПРИВ'ЯЗУЄМО ТЕГИ (УРОКИ)
        if 'topic_tags' in data:
            for tag_name in data['topic_tags']:
                # Шукаємо урок, назва якого містить цей тег (наприклад "2. Відношення, пропорції та відсотки")
                material = StudyMaterial.objects.filter(title__icontains=tag_name).first()
                if material:
                    q.materials.add(material)
                else:
                    print(f"⚠️ Увага: Урок з назвою '{tag_name}' не знайдено в базі! Завдання прив'язано без нього.")

        # 3. Логіка для тестових запитань
        if data['type'] == 'CHOICE':
            for opt_text, is_correct in data['options']:
                AnswerOption.objects.create(question=q, text=opt_text, is_correct=is_correct)

        # 4. Логіка для відповідностей
        elif data['type'] == 'MATCH':
            created_options = {}
            for opt_text in data['options']:
                opt_obj = AnswerOption.objects.create(question=q, text=opt_text, is_correct=False)
                created_options[opt_text] = opt_obj

            for left_text, right_correct_text in data['matches']:
                correct_opt_obj = created_options[right_correct_text]
                MatchItem.objects.create(question=q, text=left_text, correct_option=correct_opt_obj)

        # 5. Логіка для короткої відповіді
        elif data['type'] == 'SHORT':
            q.correct_short_answer = data['answer']
            q.save()

        count += 1

    print(f"✅ Успішно завантажено {count} завдань у базу!")


if __name__ == '__main__':
    run()