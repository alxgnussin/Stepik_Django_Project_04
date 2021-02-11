from django.contrib.auth.models import User
from django.db.models import Model, CharField, ImageField, TextField, IntegerField, ForeignKey, CASCADE, DateField

from junior_developers.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Specialty(Model):
    code = CharField(max_length=20)
    title = CharField(max_length=20)
    picture = ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'
        ordering = ['title']


class Company(Model):
    title = CharField(max_length=20)
    location = CharField(max_length=20)
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


class Application(Model):
    written_username = CharField(max_length=20)
    written_phone = CharField(max_length=20)
    written_cover_letter = TextField()
    vacancy = ForeignKey(Vacancy, on_delete=CASCADE, related_name='applications')
    user = ForeignKey(User, on_delete=CASCADE, related_name='applications', null=True)


class Status(Model):
    title = CharField(max_length=32)


class Grade(Model):
    title = CharField(max_length=20)


class Resume(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='resumes')
    status = ForeignKey(Status, on_delete=CASCADE, related_name='resumes')
    grade = ForeignKey(Grade, on_delete=CASCADE, related_name='resumes')
    specialty = ForeignKey(Specialty, on_delete=CASCADE, related_name='resume')
    salary = IntegerField()
    education = TextField()
    experience = TextField()
    portfolio = CharField(max_length=255)

