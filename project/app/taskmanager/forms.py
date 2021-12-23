from typing import ParamSpecArgs
from datetime import timedelta
from .models import Tasck
from django.forms import ModelForm, ValidationError
#from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS


class TasckForm(ModelForm):
    class Meta:
        model = Tasck
        fields = [
            "tasckTitle",
            "tasckDescription",
            "tasckStartOfTheEventDate",
            "tasckStartOfTheEventTime",
            "tasckDuration",
            "tasckPlace",
            "tasckTravelTime",
            "tasckStatus",
            "tasckStatusPeriodical",
            "tasckPeriodical",
            "tasckId"
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tasckTitle"].widget.attrs.update({
            "class": "input-text",
            "placeholder": "Название задачи",
            "size": "50"
        })
        self.fields["tasckDescription"].required = False
        self.fields["tasckDescription"].widget.attrs.update({
            "class": "input-text",
            "placeholder": "Описание задачи",
            "size": "50",
        })
        self.fields["tasckStartOfTheEventDate"].widget.attrs.update({
            "type": "datetime",
            "id": "datepicker",
            "class": "date-text",
            "placeholder": "Начало мероприятия (день.месяц.год)",
            "size": "50",
        })
        self.fields["tasckStartOfTheEventTime"].widget.attrs.update({
            "type": "datetime",
            "class": "date-text",
            "placeholder": "Начало мероприятия (часы:минуты:секунды)",
            "size": "50",
        })
        self.fields["tasckDuration"].widget.attrs.update({
            "type": "time",
            "class": "input-text",
            "placeholder": "Продолжительность мероприятия (часы:минуты:секунды)",
            "size": "50"
        })
        self.fields["tasckPlace"].widget.attrs.update({
            "class": "input-text",
            "placeholder": "Место проведения мероприятия мероприятия",
            "size": "50"
        })
        self.fields["tasckTravelTime"].widget.attrs.update({
            "type": "time",
            "class": "input-text",
            "placeholder": "Время на дорогу (часы:минуты:секунды)",
            "size": "50"
        })
        self.fields["tasckStatus"].widget.attrs.update({
            "class": "input-chack checkbox__input",
            "id": "tasckStatus",
            "size": "50",
            "onchange":"fun1()"
        })
        self.fields["tasckStatusPeriodical"].required = False
        self.fields["tasckStatusPeriodical"].widget.attrs.update({
            "class": "input-chack",
            "id": "tasckStatus",
            "size": "50",
            "onchange": "fun1()",
            "id": "tasckStatusPeriodical",
        })
        self.fields["tasckPeriodical"].required = False
        self.fields["tasckPeriodical"].widget.attrs.update({
            "type": "time",
            "class": "input-text hidden",
            "placeholder": "Период следующего напоминания (дни часы:минуты:секунды)",
            "size": "50",
            "id": "tasckPeriodical"
        })
        self.fields["tasckId"].required = False

    def clean_tasckTitle(self):
        tasckTitle = self.cleaned_data["tasckTitle"]
        if str(tasckTitle).isupper():
            return str(tasckTitle).lower()
        return tasckTitle

    def clean_tasckDescription(self):
        tasckDescription = self.cleaned_data["tasckDescription"]
        if str(tasckDescription).isupper():
            return str(tasckDescription).lower()
        return tasckDescription

    def clean_tasckPlace(self):
        tasckPlace = self.cleaned_data["tasckPlace"]
        if str(tasckPlace).isupper():
            return str(tasckPlace).lower()
        return tasckPlace

    def clean(self):
        cleaned_data = super().clean()
        tasckStartOfTheEventDate = self.cleaned_data["tasckStartOfTheEventDate"]
        try:
            tasckDuration = self.cleaned_data["tasckDuration"]
        except KeyError:
            self.add_error(None, "Неправильно введена продолжительность мероприятия")
        try:
            tasckTravelTime = self.cleaned_data["tasckTravelTime"]
        except KeyError:
            self.add_error(None, "Неправильно введено время на дорогу")
        try:
            tasckStartOfTheEventTime = self.cleaned_data["tasckStartOfTheEventTime"]
            tasckStartOfTheEventTime1 = timedelta(seconds=tasckStartOfTheEventTime.second, minutes=tasckStartOfTheEventTime.minute, hours=tasckStartOfTheEventTime.hour)
        except KeyError:
            self.add_error(None, "Неправильно введено время на дорогу")
        tasckId = self.cleaned_data["tasckId"]
        for i in range(1, len(Tasck.objects.all())+1):
            task = Tasck.objects.get(tasckId=i)
            if not task.tasckStatus and len(Tasck.objects.all())>1 and tasckId != i:
                if tasckStartOfTheEventDate == task.tasckStartOfTheEventDate:
                    if tasckStartOfTheEventTime1 <= timedelta(seconds=task.tasckStartOfTheEventTime.second, minutes=task.tasckStartOfTheEventTime.minute, hours=task.tasckStartOfTheEventTime.hour) <= tasckStartOfTheEventTime1 + tasckDuration + tasckTravelTime*2:
                        self.add_error(None, ("Ваша задача накладывается на другую задачу: "+str(task)))
        return cleaned_data

    def clean_tasckPeriodical(self):
        tasckPeriodical = self.cleaned_data.get("tasckPeriodical")
        tasckPeriodical = str(tasckPeriodical)
        if tasckPeriodical.isupper():
            return str(tasckPeriodical).lower()
        else:
            try:
                tasckPeriodical = tasckPeriodical.split()
                print(tasckPeriodical)
                if len(tasckPeriodical) > 0 and tasckPeriodical[0] != 'None':
                    if "день" in tasckPeriodical[1].lower() or "дня" in tasckPeriodical[1].lower() or "дней" in tasckPeriodical[1].lower():
                        tasckPeriodical = timedelta(days=int(tasckPeriodical[0]))
                    elif "месяц" in tasckPeriodical[1].lower() or "месяцев" in tasckPeriodical[1].lower() or "месяца" in tasckPeriodical[1].lower():
                        tasckPeriodical = timedelta(days=round(int(tasckPeriodical[0])*30.4167))
                    elif "год" in tasckPeriodical[1].lower() or "года" in tasckPeriodical[1].lower() or "лет" in tasckPeriodical[1].lower():
                        tasckPeriodical = timedelta(days=round(int(tasckPeriodical[0])*365.25))
                    elif "час" in tasckPeriodical[1].lower() or "часа" in tasckPeriodical[1].lower() or "часов" in tasckPeriodical[1].lower():
                        tasckPeriodical = timedelta(hours=round(int(tasckPeriodical[0])))
                    elif "минута" in tasckPeriodical[1].lower() or "минут" in tasckPeriodical[1].lower() or "минуты" in tasckPeriodical[1].lower():
                        tasckPeriodical = timedelta(minutes=round(int(tasckPeriodical[0])))
                    elif "неделя" in tasckPeriodical[1].lower() or "недели" in tasckPeriodical[1].lower() or "недель" in tasckPeriodical[1].lower():
                        tasckPeriodical = timedelta(days=round(int(tasckPeriodical[0]))*7)
                    else:
                        try:
                            int(tasckPeriodical[0])
                            tmp = 0
                            for i in tasckPeriodical[-1].split(":"):
                                tmp = int(i)
                        except ValueError:
                            self.add_error(None, "Ошибка, неправильно введён период повторения задачи")
                else:
                    return None
            except ValueError:
                self.add_error(None, "Ошибка, неправильно введён период повторения задачи")
        return tasckPeriodical

    def clean_tasckId(self):
        data = self.cleaned_data["tasckId"]
        data = len(Tasck.objects.all())+1
        return data
