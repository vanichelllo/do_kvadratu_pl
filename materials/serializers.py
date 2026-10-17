from rest_framework import serializers
from .models import StudyMaterial

class StudyMaterialSerializer(serializers.ModelSerializer):
    # Назва теми з класифікатора; ім'я поля лишаємо, бо бот уже на нього розрахований
    category_name = serializers.CharField(source='curriculum_topic.name', read_only=True, default=None)

    class Meta:
        model = StudyMaterial
        # Вказуємо, які саме поля хочемо віддавати боту
        fields = ['id', 'title', 'price', 'category_name']
class PurchasedMaterialSerializer(serializers.ModelSerializer):
    # Створюємо кастомне поле, якого немає в базі даних, але яке потрібне боту
    download_link = serializers.SerializerMethodField()

    class Meta:
        model = StudyMaterial
        fields = ['id', 'title', 'download_link']

    # Функція, яка генерує значення для поля download_link
    def get_download_link(self, obj):
        return f'/download/{obj.id}/'