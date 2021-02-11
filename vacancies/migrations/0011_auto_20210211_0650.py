# Generated by Django 3.1.5 on 2021-02-11 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0010_resume_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='phone',
            field=models.CharField(default='+7', max_length=20),
        ),
    ]
