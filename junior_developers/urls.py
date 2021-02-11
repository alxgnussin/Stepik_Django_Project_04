"""junior_developers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from vacancies.authentication import register_view, auth_view, logout_view
from vacancies.main import main_view, jobs_views, company_view, vacancy_view, custom_handler404, custom_handler500
from vacancies.user import my_company_view, my_company_form_view, my_vacancies_list_view, my_vacancy_form_view, \
    my_resume_list_view, my_resume_form_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main'),
    path('vacancies/<str:specialty_code>', jobs_views, name='vacancies'),
    path('vacancies', jobs_views, name='vacancies_all'),
    path('company/<int:company_id>', company_view, name='company'),
    path('vacancy/<int:job_id>', vacancy_view, name='vacancy'),
    path('signup', register_view, name='signup'),
    path('login', auth_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('my_company', my_company_view, name='my_company'),
    path('my_company_form', my_company_form_view, name='my_company_form'),
    path('my_vacancy_list', my_vacancies_list_view, name='my_vacancy_list'),
    path('my_vacancy_form', my_vacancy_form_view, name='my_vacancy_create'),
    path('my_vacancy_form/<int:job_id>', my_vacancy_form_view, name='my_vacancy_form'),
    path('my_resumes_list', my_resume_list_view, name='resumes'),
    path('my_resume_form', my_resume_form_view, name='my_resume_create'),
    path('my_resume_form/<int:resume_id>', my_resume_form_view, name='my_resume_form'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_handler404
handler500 = custom_handler500
