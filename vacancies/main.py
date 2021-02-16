from django.contrib.auth import get_user
from django.db.models import Count, Q
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render
from django.views import View

from vacancies.forms import ApplicationForm
from vacancies.models import Specialty, Company, Vacancy, Application


class MainView(View):

    def get(self, request):
        specialties = Specialty.objects.annotate(num_vacancy=Count('vacancies')).all()
        companies = Company.objects.annotate(num_vacancy=Count('vacancies')).all()

        return render(request, 'vacancies/main/index.html', {
            'specialties': specialties,
            'companies': companies
        })


class JobsView(View):

    def get(self, request, specialty_code=None):
        specialty = None
        if specialty_code:
            try:
                specialty = Specialty.objects.get(code=specialty_code)
            except:
                raise Http404()
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


class CompanyView(View):

    def get(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)
        except:
            raise Http404()
        vacancies = Vacancy.objects.filter(company__id=company_id).all()

        return render(request, 'vacancies/main/company.html', {
            'company': company,
            'vacancies': vacancies,
        })


class CompanyListView(View):

    def get(self, request):
        companies = Company.objects.annotate(num_vacancy=Count('vacancies')).all()

        return render(request, 'vacancies/main/companies.html', {'companies': companies})


class VacancyView(View):
    vacancy = None
    user = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.vacancy = Vacancy.objects.get(id=kwargs['job_id'])
        except:
            raise Http404()
        self.user = get_user(request)
        return super(VacancyView, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        form = ApplicationForm()
        if not self.user.is_anonymous:
            written_username = f'{self.user.first_name} {self.user.last_name}'
            form.initial = {
                'written_username': written_username
            }

        return render(request, 'vacancies/main/vacancy.html', {'vacancy': self.vacancy, 'form': form})

    def post(self, request, job_id):
        form = ApplicationForm(request.POST)
        if not form.is_valid():
            return render(request, 'vacancies/main/vacancy.html', {'vacancy': self.vacancy, 'form': form})
        if self.user.is_anonymous:
            user = None
        else:
            user = self.user
        Application.objects.create(
            written_username=form.cleaned_data['written_username'],
            written_phone=form.cleaned_data['written_phone'],
            written_cover_letter=form.cleaned_data['written_cover_letter'],
            vacancy=self.vacancy,
            user=user
        )

        return render(request, 'vacancies/main/sent.html', {'job_id': job_id})


def custom_handler404(request, exception):
    return HttpResponseNotFound('<br/><h1>Ошибка 404</h1><h2>Запрашиваемый ресурс не найден</h2>')


def custom_handler500(request):
    return HttpResponseServerError('<br/><h1>Ошибка 500</h1><h2>Ошибка запроса. Отказано в обработке</h2>')
