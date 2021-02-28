from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from vacancies.forms import CompanyForm, VacancyForm, ResumeForm
from vacancies.models import Company, Vacancy, Resume


class MyCompaniesList(ListView, LoginRequiredMixin):
    template_name = 'vacancies/user/companies.html'

    def get_queryset(self):
        queryset = Company.objects.filter(owner=self.request.user).all()
        if not queryset:
            return render(self.request, 'vacancies/user/company_create.html')
        return queryset




# @login_required
# def my_company_view(request):
#     user = request.user
#     if not user.companies.all():
#         return render(request, 'vacancies/user/company_create.html')
#     return redirect('my_company_form')


class MyCompanyForm(View, LoginRequiredMixin):

    @staticmethod
    def get_company(request):
        user = request.user
        company = user.companies.first()
        return company

    def get(self, request):
        form = CompanyForm()
        company = self.get_company(request)
        if company:
            form.initial = {
                'title': company.title,
                'location': company.location,
                'description': company.description,
                'employee_count': company.employee_count,
            }
            return render(request, 'vacancies/user/company_edit.html', {'form': form, 'logo': company.logo})
        return render(request, 'vacancies/user/company_edit.html', {'form': form})

    def post(self, request):
        form = CompanyForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'vacancies/user/company_edit.html', {'form': form})

        company = self.get_company(request)

        if company:
            company.title = form.cleaned_data['title']
            company.location = form.cleaned_data['location']
            if form.cleaned_data['logo']:
                company.logo = form.cleaned_data['logo']
            company.description = form.cleaned_data['description']
            company.employee_count = form.cleaned_data['employee_count']
            company.owner = get_user(request)
        else:
            company = Company(
                title=form.cleaned_data['title'],
                location=form.cleaned_data['location'],
                logo=form.cleaned_data['logo'],
                description=form.cleaned_data['description'],
                employee_count=form.cleaned_data['employee_count'],
                owner=get_user(request),
            )
        company.save()
        return redirect(reverse('my_company_form') + '?submitted=True')


@login_required
def my_vacancies_list_view(request):
    user = request.user
    user_company = user.companies.first()
    vacancies_list = None
    if user_company:
        vacancies_list = user_company.vacancies.annotate(res_count=Count('applications')).all()

    return render(request, 'vacancies/user/vacancy_list.html', {'vacancies': vacancies_list})


class MyVacancyForm(View, LoginRequiredMixin):

    @staticmethod
    def get_vacancy(request, job_id):
        user = request.user
        vacancy = Vacancy.objects.filter(id=job_id, company__owner__id=user.id).first()
        return vacancy

    def get(self, request, job_id=None):
        vacancy = None

        if job_id:
            vacancy = self.get_vacancy(request, job_id)

        form = VacancyForm()

        if vacancy:
            form.initial = {
                'title': vacancy.title,
                'specialty': vacancy.specialty,
                'skills': vacancy.skills,
                'description': vacancy.description,
                'salary_min': vacancy.salary_min,
                'salary_max': vacancy.salary_max,
            }

        return render(request, 'vacancies/user/vacancy_edit.html', {'form': form})

    def post(self, request, job_id=None):
        user = request.user
        user_company = user.companies.first()
        vacancy = None

        if job_id:
            vacancy = self.get_vacancy(request, job_id)

        form = VacancyForm(request.POST)

        if not form.is_valid():
            return render(request, 'vacancies/user/vacancy_edit.html', {'form': form})

        if vacancy:
            vacancy.title = form.cleaned_data['title']
            vacancy.specialty = form.cleaned_data['specialty']
            vacancy.skills = form.cleaned_data['skills']
            vacancy.description = form.cleaned_data['description']
            vacancy.salary_min = form.cleaned_data['salary_min']
            vacancy.salary_max = form.cleaned_data['salary_max']
        else:
            vacancy = Vacancy(
                title=form.cleaned_data['title'],
                specialty=form.cleaned_data['specialty'],
                skills=form.cleaned_data['skills'],
                description=form.cleaned_data['description'],
                salary_min=form.cleaned_data['salary_min'],
                salary_max=form.cleaned_data['salary_max'],
                company=user_company,
            )
        vacancy.save()
        return redirect(reverse('my_vacancy_form', args=[vacancy.id]) + '?submitted=True')


@login_required
def my_resume_list_view(request):
    user = request.user
    resumes_list = user.resumes.all()
    if len(resumes_list) > 0:
        return render(request, 'vacancies/user/resumes.html', {'resumes_list': resumes_list})
    return render(request, 'vacancies/user/resume_create.html')


class MyResumeForm(View, LoginRequiredMixin):

    @staticmethod
    def get_resume(request, resume_id):
        user = request.user
        resume = Resume.objects.filter(id=resume_id, user__id=user.id).first()
        return resume

    def get(self, request, resume_id=None):
        resume = None
        if resume_id:
            resume = self.get_resume(request, resume_id)

        form = ResumeForm()
        if resume:
            form.initial = {
                'status': resume.status,
                'grade': resume.grade,
                'specialty': resume.specialty,
                'salary': resume.salary,
                'education': resume.education,
                'experience': resume.experience,
                'portfolio': resume.portfolio,
                'title': resume.title,
                'phone': resume.phone,
                'email': resume.email,
            }

        return render(request, 'vacancies/user/resume_edit.html', {'form': form})

    def post(self, request, resume_id=None):
        resume = None
        if resume_id:
            resume = self.get_resume(request, resume_id)

        form = ResumeForm(request.POST)

        if not form.is_valid():
            return render(request, 'vacancies/user/resume_edit.html', {'form': form})

        if resume:
            resume.status = form.cleaned_data['status']
            resume.grade = form.cleaned_data['grade']
            resume.specialty = form.cleaned_data['specialty']
            resume.salary = form.cleaned_data['salary']
            resume.education = form.cleaned_data['education']
            resume.experience = form.cleaned_data['experience']
            resume.portfolio = form.cleaned_data['portfolio']
            resume.title = form.cleaned_data['title']
            resume.phone = form.cleaned_data['phone']
            resume.email = form.cleaned_data['email']
        else:
            resume = Resume(
                user=get_user(request),
                status=form.cleaned_data['status'],
                grade=form.cleaned_data['grade'],
                specialty=form.cleaned_data['specialty'],
                salary=form.cleaned_data['salary'],
                education=form.cleaned_data['education'],
                experience=form.cleaned_data['experience'],
                portfolio=form.cleaned_data['portfolio'],
                title=form.cleaned_data['title'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
            )
        resume.save()
        return redirect(reverse('resumes'))


@login_required
def applications_list_view(request, job_id):
    user = request.user
    vacancy = Vacancy.objects.filter(id=job_id, company__owner__id=user.id).first()
    applications = vacancy.applications.all()

    return render(request, 'vacancies/user/applications_list.html', {
        'applications': applications,
        'job_title': vacancy.title,
    })
