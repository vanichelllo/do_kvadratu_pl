from django import forms
from .models import StudentReport, CurriculumTopic # Додаємо імпорт

class StudentReportForm(forms.ModelForm):
    # Кастомізуємо поле вибору, щоб у списку було видно повний шлях до теми
    curriculum_topic = forms.ModelChoiceField(
        queryset=CurriculumTopic.objects.select_related('chapter__grade').all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Тема уроку",
        required=True
    )

    class Meta:
        model = StudentReport
        # Змінили 'topic' на 'curriculum_topic'
        fields = ['curriculum_topic', 'nush_modeling', 'nush_solving', 'nush_analysis', 'homework_status', 'teacher_comment']
        widgets = {
            'nush_modeling': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12, 'value': 0}),
            'nush_solving': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12, 'value': 0}),
            'nush_analysis': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12, 'value': 0}),
            'homework_status': forms.Select(attrs={'class': 'form-control'}),
            'teacher_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Пару слів про успіхи...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Робимо так, щоб у списку писало, наприклад: "8 клас - Квадратні рівняння -> Теорема Вієта"
        self.fields['curriculum_topic'].label_from_instance = lambda obj: f"{obj.chapter.grade.name} | {obj.chapter.name} -> {obj.name}"

    def clean(self):
        cleaned_data = super().clean()
        for field in ('nush_modeling', 'nush_solving', 'nush_analysis'):
            value = cleaned_data.get(field)
            if value is not None and not 1 <= value <= 12:
                self.add_error(field, "Оцінка має бути від 1 до 12.")
        return cleaned_data