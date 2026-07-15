from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувач з таким email вже зареєстрований. Увійдіть у систему!")
        return email

    def save(self, commit=True):
        # 1. Створюємо об'єкт користувача, але поки НЕ записуємо в базу (commit=False)
        user = super().save(commit=False)

        # 2. Копіюємо унікальний email у поле username
        user.username = user.email

        # 3. Тепер безпечно зберігаємо в базу даних
        if commit:
            user.save()
        return user

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