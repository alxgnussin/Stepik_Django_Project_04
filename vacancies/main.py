from django.contrib.auth import get_user
from django.db.models import Count, Q
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

from vacancies.forms import ApplicationForm
from vacancies.models import Specialty, Company, Vacancy, Application


def main_view(request):
    specialties = Specialty.objects.annotate(num_vacancy=Count('vacancies')).all()
    companies = Company.objects.annotate(num_vacancy=Count('vacancies')).all()

    return render(request, 'vacancies/main/index.html', {
        'specialties': specialties,
        'companies': companies,
    })


def jobs_views(request, specialty_code=None):
    specialty = None
    if specialty_code:
        specialty = Specialty.objects.get_object_or_404(code=specialty_code)
        vacancies = Vacancy.objects.filter(specialty__code=specialty_code).all()
    else:
        search = request.GET.get('query')
        if search:
            vacancies = Vacancy.objects.filter(Q(skills__icontains=search) | Q(title__icontains=search)).all()
        else:
            vacancies = Vacancy.objects.all()

    return render(request, 'vacancies/main/vacancies.html', {
        'vacancies': vacancies,
        'specialty_code': specialty_code,
        'specialty': specialty,
    })


def company_view(request, company_id):
    company = Company.objects.get_object_or_404(id=company_id)
    vacancies = Vacancy.objects.filter(company__id=company_id).all()

    return render(request, 'vacancies/main/company.html', {
        'company': company,
        'vacancies': vacancies,
    })


def company_list_view(request):
    companies = Company.objects.annotate(num_vacancy=Count('vacancies')).all()
    return render(request, 'vacancies/main/companies.html', {'companies': companies})


def vacancy_view(request, job_id):
    vacancy = Vacancy.objects.get_object_or_404(id=job_id)
    user = get_user(request)
    if request.method == 'GET':
        form = ApplicationForm()
        if not user.is_anonymous:
            written_username = f'{user.first_name} {user.last_name}'
            form.initial = {
                'written_username': written_username,
            }
            return render(request, 'vacancies/main/vacancy.html', {'vacancy': vacancy, 'form': form})

    form = ApplicationForm(request.POST)
    if not form.is_valid():
        return render(request, 'vacancies/main/vacancy.html', {'vacancy': vacancy, 'form': form})
    if user.is_anonymous:
        user = None
    Application.objects.create(
        written_username=form.cleaned_data['written_username'],
        written_phone=form.cleaned_data['written_phone'],
        written_cover_letter=form.cleaned_data['written_cover_letter'],
        vacancy=vacancy,
        user=user,
    )

    return render(request, 'vacancies/main/sent.html', {'job_id': job_id})


def custom_handler404(request, exception):
    return HttpResponseNotFound('<br/><h1>Ошибка 404</h1><h2>Запрашиваемый ресурс не найден</h2>')


def custom_handler500(request):
    return HttpResponseServerError('<br/><h1>Ошибка 500</h1><h2>Ошибка запроса. Отказано в обработке</h2>')
