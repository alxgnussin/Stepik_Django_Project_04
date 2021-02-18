from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from vacancies.forms import RegisterForm, LoginForm, ProfileForm, ChangePasswordForm
from vacancies.models import Profile
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
            username=username, first_name=first_name, last_name=last_name, password=password,
        )
    except IntegrityError:
        error_msg = 'Такой логин уже существует!'
        return render(request, 'vacancies/auth/register.html', {'form': form, 'message': error_msg})
    return redirect('login')


@user_passes_test(anonymous_check, login_url='/')
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


@login_required
def logout_view(request):
    logout(request)
    return redirect('main')


class MyProfileForm(View, LoginRequiredMixin):

    def get(self, request):
        user = get_user(request)
        profile = Profile.objects.filter(user=user).first()
        form = ProfileForm()
        form.initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        if profile:
            form.initial = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': profile.phone,
            }
        return render(request, 'vacancies/auth/profile.html', {'form': form})

    def post(self, request):
        user = get_user(request)
        profile = Profile.objects.filter(user=user).first()

        form = ProfileForm(request.POST)
        if not form.is_valid():
            return render(request, 'vacancies/auth/profile.html', {'form': form})
        if profile:
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            profile.phone = form.cleaned_data['phone']
            profile.user = user
        else:
            user.email = form.cleaned_data['email']
            profile = Profile(
                user=user,
                phone=form.cleaned_data['phone'],
            )
        user.save()
        profile.save()
        return redirect(reverse('profile') + '?submitted=True')


class ChangePassword(View, LoginRequiredMixin):

    def get(self, request):
        form = ChangePasswordForm()
        return render(request, 'vacancies/auth/change_pass.html', {'form': form})

    def post(self, request):
        user = get_user(request)
        form = ChangePasswordForm(request.POST)

        if not form.is_valid():
            return render(request, 'vacancies/auth/change_pass.html', {'form': form})

        current_pass = form.cleaned_data['current_password']
        new_password = form.cleaned_data['password']

        if check_password(current_pass, user.password):
            user.set_password(new_password)
            user.save()
            user = authenticate(request, username=user.username, password=new_password)
            login(request, user)
        else:
            return redirect(reverse('change_password') + '?no_change=True')

        return redirect(reverse('change_password') + '?submitted=True')
