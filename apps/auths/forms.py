from django import forms
from auths.models import CustomUser
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Введите пароль'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label='Повторите пароль'
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('password_confirm')

        if password != repeat_password:
            raise ValidationError(
                'Пароли не совпадают'
            )

    class Meta:
        model = CustomUser
        fields = ['login', "first_name"]


class LoginForm(forms.Form):
    login = forms.CharField(
        label='Логин'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Введите пароль'
    )