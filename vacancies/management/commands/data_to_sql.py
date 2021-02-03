from django.core.management.base import BaseCommand

from dotmap import DotMap

from vacancies.data import specialties, companies, jobs
from vacancies.models import Specialty, Company, Vacancy


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for direction in specialties:
            item = DotMap(direction)
            new_item = Specialty(
                code=item.code,
                title=item.title,
                picture=item.picture
            )
            new_item.save()

        for company in companies:
            item = DotMap(company)
            new_item = Company(
                id=item.id,
                title=item.title,
                location=item.location,
                logo=item.logo,
                description=item.description,
                employee_count=item.employee_count
            )
            new_item.save()

        for job in jobs:
            item = DotMap(job)
            direction = Specialty.objects.filter(code=item.specialty).first()
            company = Company.objects.get(id=item.company)
            new_item = Vacancy(
                id=item.id,
                title=item.title,
                specialty=direction,
                company=company,
                skills=item.skills,
                description=item.description,
                salary_min=item.salary_from,
                salary_max=item.salary_to,
                posted=item.posted
            )
            new_item.save()

