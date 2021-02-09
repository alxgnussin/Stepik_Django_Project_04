from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from vacancies.forms import CompanyForm
from vacancies.models import Company


@login_required
def vacancy_send_view(request, vacancy_id):
    user = get_user(request)
    pass


@login_required
def my_company_view(request):
    user = get_user(request)
    if not user.companies.all():
        return render(request, 'vacancies/user/company_create.html')
    return redirect('my_company_form')


@login_required
def my_company_form_view(request):
    user = get_user(request)
    company = Company.objects.filter(owner=user).first()
    if request.method == 'GET':
        form = CompanyForm()
        if company:
            form.initial = {
                'title': company.title,
                'location': company.location,
                'description': company.description,
                'employee_count': company.employee_count
            }
        return render(request, 'vacancies/user/company_edit.html', {'form': form, 'logo': company.logo})

    form = CompanyForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'vacancies/user/company_edit.html', {'form': form})

    title = form.cleaned_data['title']
    location = form.cleaned_data['location']
    logo = form.cleaned_data['logo']
    description = form.cleaned_data['description']
    employee_count = form.cleaned_data['employee_count']
    owner = user
    if company:
        company.title = title
        company.location = location
        if logo:
            company.logo = logo
        company.description = description
        company.employee_count = employee_count
        company.owner = owner
    else:
        company = Company(
            title=title,
            location=location,
            logo=logo,
            description=description,
            employee_count=employee_count,
            owner=owner
        )
    company.save()
    return redirect(reverse('my_company_form') + '?submitted=True')


@login_required
def my_vacancies_view(request):
    pass


@login_required
def my_vacancy_view(request, vacancy_id):
    pass
