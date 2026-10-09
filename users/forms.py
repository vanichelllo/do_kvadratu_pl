from django import forms
from .models import CustomUser


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'role', 'target_grade']

        widgets = {
            'first_name': forms.TextInput(
                attrs={'style': 'width: 100%; padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px;',
                       'placeholder': "Ім'я"}),
            'last_name': forms.TextInput(
                attrs={'style': 'width: 100%; padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px;',
                       'placeholder': 'Прізвище'}),
            'phone_number': forms.TextInput(
                attrs={'style': 'width: 100%; padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px;',
                       'placeholder': '+380...'}),
            'role': forms.Select(
                attrs={'style': 'width: 100%; padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px;'}),
            'target_grade': forms.Select(
                attrs={'style': 'width: 100%; padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px;'}),
        }