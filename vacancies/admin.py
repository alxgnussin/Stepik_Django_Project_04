from django.contrib import admin

from .models import Specialty, Company, Vacancy, Application, Status, Grade, Resume, Profile


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'title', 'picture')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'location',
        'logo',
        'description',
        'employee_count',
        'owner',
    )
    list_filter = ('owner',)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'specialty',
        'company',
        'skills',
        'description',
        'salary_min',
        'salary_max',
        'posted',
    )
    list_filter = ('specialty', 'company', 'posted')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'written_username',
        'written_phone',
        'written_cover_letter',
        'vacancy',
        'user',
    )
    list_filter = ('vacancy', 'user')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'grade',
        'specialty',
        'salary',
        'education',
        'experience',
        'portfolio',
        'title',
        'phone',
        'email',
    )
    list_filter = ('user', 'status', 'grade', 'specialty')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone')
    list_filter = ('user',)
