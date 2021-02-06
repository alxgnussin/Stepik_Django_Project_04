from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20, label='Логин')
    first_name = forms.CharField(max_length=20, label='Имя')
    last_name = forms.CharField(max_length=20, label='Фамилия')
    password = forms.CharField(max_length=20, label='Пароль')


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20, label='Логин')
    password = forms.CharField(max_length=20, label='Пароль')
