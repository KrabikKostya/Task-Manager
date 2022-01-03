from django.db import models
class Tasck(models.Model):
    tasckTitle = models.CharField("Название задачи", max_length=100)
    tasckDescription = models.CharField("Описание задачи", max_length=500)
    tasckStartOfTheEventTime = models.TimeField("Время начала мероприятия")
    tasckDuration = models.DurationField("Продолжительность input-text")
    tasckPlace = models.CharField("Место проведения мероприятия", max_length=200)
    tasckTravelTime = models.DurationField("Время на дорогу")
    tasckStatus = models.BooleanField("Задача выполнена ?")
    tasckStartOfTheEventDate = models.DateField("Дата начала мероприятия")
    tasckStatusPeriodical = models.BooleanField("Задача переодическая ?")
    tasckPeriodical = models.CharField("Период, через который нужно напоминать", null=True, max_length=100)
    tasckId = models.IntegerField("ID задачи", null=True)
    isDelate = models.BooleanField("Задача удалена ?")
    def __str__(self):
        return self.tasckTitle
