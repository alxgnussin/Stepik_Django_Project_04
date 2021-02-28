from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Model, CharField, ImageField, TextField, IntegerField, ForeignKey, CASCADE, DateField, \
    EmailField

from junior_developers.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Specialty(Model):
    code = CharField(max_length=20)
    title = CharField(max_length=50)
    picture = ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'
        ordering = ['title']


class Company(Model):
    title = CharField(max_length=50)
    location = CharField(max_length=50)
    logo = ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, null=True)
    description = TextField()
    employee_count = IntegerField()
    owner = ForeignKey(User, on_delete=CASCADE, related_name='companies', null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['title']


class Vacancy(Model):
    title = CharField(max_length=50)
    specialty = ForeignKey(Specialty, on_delete=CASCADE, related_name='vacancies')
    company = ForeignKey(Company, on_delete=CASCADE, related_name='vacancies')
    skills = TextField()
    description = TextField()
    salary_min = IntegerField()
    salary_max = IntegerField()
    posted = DateField(auto_now=True)
    location = CharField(max_length=100, default='', verbose_name='Регион, город')

    def clean(self):
        if self.salary_min > self.salary_max:
            raise ValidationError('Минимальная зарплата не может быть больше максимальной')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['title']


class Application(Model):
    written_username = CharField(max_length=50)
    written_phone = CharField(max_length=20)
    written_cover_letter = TextField()
    vacancy = ForeignKey(Vacancy, on_delete=CASCADE, related_name='applications')
    user = ForeignKey(User, on_delete=CASCADE, related_name='applications', null=True)

    def __str__(self):
        return self.title


class Status(Model):
    title = CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статус соискателя'
        verbose_name_plural = 'Статусы соискателя'
        ordering = ['title']


class Grade(Model):
    title = CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Квалификация'
        verbose_name_plural = 'Квалификации'
        ordering = ['title']


class Resume(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='resumes')
    status = ForeignKey(Status, on_delete=CASCADE, related_name='resumes')
    grade = ForeignKey(Grade, on_delete=CASCADE, related_name='resumes')
    specialty = ForeignKey(Specialty, on_delete=CASCADE, related_name='resume')
    salary = IntegerField()
    education = TextField()
    experience = TextField()
    portfolio = CharField(max_length=255, null=True)
    title = CharField(max_length=50, default='Резюме по умолчанию')
    phone = CharField(max_length=20, default='+7')
    email = EmailField(null=True)

    def __str__(self):
        return self.title


class Profile(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='profile')
    phone = CharField(max_length=20, null=True)

    def __str__(self):
        return self.title
