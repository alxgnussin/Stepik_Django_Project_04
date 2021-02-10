from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from vacancies.forms import CompanyForm, VacancyForm
from vacancies.models import Company, Vacancy, Application


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
    company = user.companies.first()
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
        return render(request, 'vacancies/user/company_edit.html', {'form': form})

    form = CompanyForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'vacancies/user/company_edit.html', {'form': form})

    # title = form.cleaned_data['title']
    # location = form.cleaned_data['location']
    # logo = form.cleaned_data['logo']
    # description = form.cleaned_data['description']
    # employee_count = form.cleaned_data['employee_count']
    # owner = user
    if company:
        company.title = form.cleaned_data['title']
        company.location = form.cleaned_data['location']
        if form.cleaned_data['logo']:
            company.logo = form.cleaned_data['logo']
        company.description = form.cleaned_data['description']
        company.employee_count = form.cleaned_data['employee_count']
        company.owner = user
    else:
        company = Company(
            title=form.cleaned_data['title'],
            location=form.cleaned_data['location'],
            logo=form.cleaned_data['logo'],
            description=form.cleaned_data['description'],
            employee_count=form.cleaned_data['employee_count'],
            owner=user
        )
    company.save()
    return redirect(reverse('my_company_form') + '?submitted=True')


@login_required
def my_vacancies_list_view(request):
    user = get_user(request)
    user_company = user.companies.first()
    vacancies_list = None
    if user_company:
        vacancies_list = user_company.vacancies.annotate(res_count=Count('applications')).all()

    return render(request, 'vacancies/user/vacancy_list.html', {'vacancies': vacancies_list})


@login_required
def my_vacancy_form_view(request, job_id=None):
    user = get_user(request)
    user_company = user.companies.first()
    vacancy = None

    if request.method == 'GET':
        form = VacancyForm()
        if job_id:
            vacancy = Vacancy.objects.filter(id=job_id).first()

        if vacancy:
            form.initial = {
                'title': vacancy.title,
                'specialty': vacancy.specialty,
                'skills': vacancy.skills,
                'description': vacancy.description,
                'salary_min': vacancy.salary_min,
                'salary_max': vacancy.salary_max,
            }

        return render(request, 'vacancies/user/vacancy_edit.html', {'form': form, 'job_id': vacancy.id})

    form = VacancyForm(request.POST)

    if not form.is_valid():
        return render(request, 'vacancies/user/vacancy_edit.html', {'form': form})

    if vacancy:
        vacancy.title = form.cleaned_data['title'],
        vacancy.specialty = form.cleaned_data['specialty'],
        vacancy.skills = form.cleaned_data['skills'],
        vacancy.description = form.cleaned_data['description'],
        vacancy.salary_min = form.cleaned_data['salary_min'],
        vacancy.salary_max = form.cleaned_data['salary_max'],
    else:
        vacancy = Vacancy(
            title=form.cleaned_data['title'],
            specialty=form.cleaned_data['specialty'],
            skills=form.cleaned_data['skills'],
            description=form.cleaned_data['description'],
            salary_min=form.cleaned_data['salary_min'],
            salary_max=form.cleaned_data['salary_max'],
            company=user_company
        )
    vacancy.save()
    return redirect(reverse('my_vacancy_form', {'job_id': vacancy.id}) + '?submitted=True')
