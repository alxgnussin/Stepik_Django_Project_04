from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse

from vacancies.forms import CompanyForm, VacancyForm, ResumeForm
from vacancies.models import Company, Vacancy, Resume


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
    applications = None

    if job_id:
        vacancy = Vacancy.objects.filter(id=job_id).first()
    if vacancy:
        applications = vacancy.applications.all()

    if request.method == 'GET':
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

        return render(request, 'vacancies/user/vacancy_edit.html', {'form': form, 'applications': applications})

    form = VacancyForm(request.POST)

    if not form.is_valid():
        return render(request, 'vacancies/user/vacancy_edit.html', {'form': form, 'applications': applications})

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
            company=user_company
        )
    vacancy.save()
    return redirect(reverse('my_vacancy_form', args=[vacancy.id]) + '?submitted=True')


@login_required
def my_resume_list_view(request):
    user = get_user(request)
    resumes_list = user.resumes.all()
    if len(resumes_list) > 0:
        return render(request, 'vacancies/user/resumes.html', {'resumes_list': resumes_list})
    return render(request, 'vacancies/user/resume_create.html')


@login_required
def my_resume_form_view(request, resume_id=None):
    user = get_user(request)
    resume = None
    if resume_id:
        resume = Resume.objects.filter(id=resume_id).first()
    if request.method == 'GET':
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
            user=user,
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
