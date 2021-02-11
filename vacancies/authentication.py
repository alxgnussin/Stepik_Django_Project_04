from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect

from vacancies.forms import RegisterForm, LoginForm
from vacancies.utility import anonymous_check


@user_passes_test(anonymous_check, login_url='/')
def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'vacancies/auth/register.html', {'form': form})

    form = RegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'vacancies/auth/register.html', {'form': form})

    username = form.cleaned_data['username']
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    password = form.cleaned_data['password']
    try:
        User.objects.create_user(
            username=username, first_name=first_name, last_name=last_name, password=password
        )
    except IntegrityError:
        error_msg = 'Такой логин уже существует!'
        return render(request, 'vacancies/auth/register.html', {'form': form, 'message': error_msg})
    return redirect('login')


def auth_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'vacancies/auth/login.html', {'form': form})

    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(request, 'vacancies/auth/login.html', {'form': form})

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return redirect('main')
    else:
        error_msg = 'Ошибка аутентификации'
        return render(request, 'vacancies/auth/login.html', {'form': form, 'message': error_msg})


def logout_view(request):
    logout(request)
    return redirect('main')
