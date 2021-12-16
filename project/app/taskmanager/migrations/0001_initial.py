# Generated by Django 3.2.9 on 2021-12-15 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tasck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tasckTitle', models.CharField(max_length=100, verbose_name='Название задачи')),
                ('tasckDescription', models.CharField(max_length=500, verbose_name='Описание задачи')),
                ('tasckStartOfTheEventTime', models.TimeField(verbose_name='Время начала мероприятия')),
                ('tasckDuration', models.DurationField(verbose_name='Продолжительность input-text')),
                ('tasckPlace', models.CharField(max_length=200, verbose_name='Место проведения мероприятия')),
                ('tasckTravelTime', models.DurationField(verbose_name='Время на дорогу')),
                ('tasckStatus', models.BooleanField(verbose_name='Задача выполнена ?')),
                ('tasckStartOfTheEventDate', models.DateField(verbose_name='Дата начала мероприятия')),
                ('tasckStatusPeriodical', models.BooleanField(verbose_name='Задача переодическая ?')),
                ('tasckPeriodical', models.DurationField(null=True, verbose_name='Период, через который нужно напоминать')),
            ],
        ),
    ]
