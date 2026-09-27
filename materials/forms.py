from django import forms
from .models import StudentReport

class StudentReportForm(forms.ModelForm):
    class Meta:
        model = StudentReport
        fields = ['topic', 'nush_modeling', 'nush_solving', 'nush_analysis', 'homework_status', 'teacher_comment']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Напр.: Системи рівнянь'}),
            'nush_modeling': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12, 'value': 0}),
            'nush_solving': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12, 'value': 0}),
            'nush_analysis': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12, 'value': 0}),
            'homework_status': forms.Select(attrs={'class': 'form-control'}),
            'teacher_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Пару слів про успіхи...'}),
        }