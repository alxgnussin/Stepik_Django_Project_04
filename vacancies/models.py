from django.contrib.auth.models import User
from django.db import models

from junior_developers.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Specialty(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'
        ordering = ['title']


class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, null=True)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies", null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['title']


class Vacancy(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    posted = models.DateField()


class Application(models.Model):
    written_username = models.CharField(max_length=20)
    written_phone = models.CharField(max_length=20)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications", null=True)
