from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import DateInput

from users.models import Player, Position, Medcine, CustomUser
import datetime


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['surname', 'firstname', 'patronymic', 'age', 'position', 'cost', 'expiration_date', 'injury_choice', 'injury_date', 'recovery_date']
        widgets = {
            'injury_date': DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'recovery_date': DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'expiration_date': DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'age': forms.NumberInput(attrs={'min': 0}),
            'cost': forms.NumberInput(attrs={'min': 0}),
        }

        input_formats = {
            'expiration_date': ['%Y-%m-%d'],
            'injury_date': ['%Y-%m-%d'],
            'recovery_date': ['%Y-%m-%d'],
        }

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        if expiration_date and expiration_date < datetime.date.today():
            raise forms.ValidationError("Дата окончания не может быть в прошлом!")
        return expiration_date


class EditForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        widgets = {
            'injury_date': DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'recovery_date': DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'expiration_date': DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'age': forms.NumberInput(attrs={'min': 0}),
            'cost': forms.NumberInput(attrs={'min': 0}),
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']

    name = forms.CharField(max_length=128, required=True)


class EditPositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'


class MedcineForm(forms.ModelForm):
    class Meta:
        model = Medcine
        fields = ['full_name', 'injury', 'injury_date', 'recovery_date']
        widgets = {
            'injury_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'recovery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_recovery_date(self):
        injury_date = self.cleaned_data.get('injury_date')
        recovery_date = self.cleaned_data.get('recovery_date')

        if injury_date and recovery_date:
            if recovery_date < injury_date:
                raise forms.ValidationError("Дата выздоровления не может быть раньше даты получения травмы!")

        return recovery_date


class EditMedcineForm(forms.ModelForm):
    class Meta:
        model = Medcine
        fields = '__all__'


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Электронная почта",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'})
    )
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'})
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )
