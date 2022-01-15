import calendar
from datetime import datetime, time, date, timedelta
from .utils import Calendar
from .models import *
from django.utils.safestring import mark_safe
from django.views import generic
from django.shortcuts import render, redirect
from .forms import TasckForm
from django.http import HttpResponseNotFound
from django.utils import timezone


def index(request):
    form = TasckForm
    periodicalTasks = Tasck.objects.all().filter(tasckStatusPeriodical=True, isDelate=False)
    m = len(Tasck.objects.all().filter(tasckStatus=True, isDelate=False))
    now = timedelta(hours=timezone.now().hour+2, minutes=timezone.now().minute, seconds=timezone.now().second)
    taskTime = None
    t = None
    for i in range(1, len(Tasck.objects.all())+1):
        t = Tasck.objects.get(id=i)
        if t in periodicalTasks:
            taskTime = timedelta(hours=t.tasckStartOfTheEventTime.hour, minutes=t.tasckStartOfTheEventTime.minute, seconds=t.tasckStartOfTheEventTime.second)
            if t.tasckStartOfTheEventDate == timezone.now().date() and taskTime <= now:
                if "day," in t.tasckPeriodical.split():
                    try:
                        t.tasckStartOfTheEventDate = date(year=t.tasckStartOfTheEventDate.year, month=t.tasckStartOfTheEventDate.month, day=t.tasckStartOfTheEventDate.day+int(t.tasckPeriodical.split()[0]))
                    except ValueError:
                        try:
                            t.tasckStartOfTheEventDate = date(year=t.tasckStartOfTheEventDate.year, month=t.tasckStartOfTheEventDate.month+1, day=t.tasckStartOfTheEventDate.day+int(t.tasckPeriodical.split()[0])-(calendar.monthrange(t.tasckStartOfTheEventDate.year, month=t.tasckStartOfTheEventDate.month+1)[1]))
                        except ValueError:
                            t.tasckStartOfTheEventDate = date(year=t.tasckStartOfTheEventDate.year+1, month=t.tasckStartOfTheEventDate.month+1-12, day=t.tasckStartOfTheEventDate.day+int(t.tasckPeriodical.split()[0])-(calendar.monthrange(t.tasckStartOfTheEventDate.year, month=t.tasckStartOfTheEventDate.month+1)[1]))
                else:
                    try:
                        t.tasckStartOfTheEventTime = time(hour=t.tasckStartOfTheEventTime.hour, minute=t.tasckStartOfTheEventTime.minute + int(t.tasckPeriodical.split()[0].split(":")[1]), second=t.tasckStartOfTheEventTime.second)
                    except ValueError:
                        try:
                            t.tasckStartOfTheEventTime = time(hour=t.tasckStartOfTheEventTime.hour + 1, minute=t.tasckStartOfTheEventTime.minute, second=t.tasckStartOfTheEventTime.second)
                        except ValueError:
                            try:
                                t.tasckStartOfTheEventTime = time(hour=t.tasckStartOfTheEventTime.hour + 1 - 24, minute=t.tasckStartOfTheEventTime.minute, second=t.tasckStartOfTheEventTime.second)
                                t.tasckStartOfTheEventDate = date(year=t.tasckStartOfTheEventDate.year, month=t.tasckStartOfTheEventDate.month, day=t.tasckStartOfTheEventDate.day+1)
                            except ValueError:
                                try:
                                    t.tasckStartOfTheEventTime = time(hour=t.tasckStartOfTheEventTime.hour + 1 - 24, minute=t.tasckStartOfTheEventTime.minute, second=t.tasckStartOfTheEventTime.second)
                                    t.tasckStartOfTheEventDate = date(year=t.tasckStartOfTheEventDate.year, month=t.tasckStartOfTheEventDate.month+1, day=t.tasckStartOfTheEventDate.day+1-(calendar.monthrange(t.tasckStartOfTheEventDate.year, month=t.tasckStartOfTheEventDate.month+1)[1]))
                                except ValueError:
                                    t.tasckStartOfTheEventTime = time(hour=t.tasckStartOfTheEventTime.hour + 1 - 24, minute=t.tasckStartOfTheEventTime.minute, second=t.tasckStartOfTheEventTime.second)
                                    t.tasckStartOfTheEventDate = date(year=t.tasckStartOfTheEventDate.year+1, month=t.tasckStartOfTheEventDate.month+1-12, day=t.tasckStartOfTheEventDate.day+1-(calendar.monthrange(t.tasckStartOfTheEventDate.year, month=t.tasckStartOfTheEventDate.month+1)[1]))
                    try:
                        t.tasckStartOfTheEventTime = time(hour=t.tasckStartOfTheEventTime.hour + int(t.tasckPeriodical.split()[0].split(":")[0]), minute=t.tasckStartOfTheEventTime.minute, second=t.tasckStartOfTheEventTime.second)
                    except ValueError:
                        try:
                            t.tasckStartOfTheEventTime = time(hour=t.tasckStartOfTheEventTime.hour + int(t.tasckPeriodical.split()[0].split(":")[0]) - 24, minute=t.tasckStartOfTheEventTime.minute, second=t.tasckStartOfTheEventTime.second)
                            t.tasckStartOfTheEventDate = date(year=t.tasckStartOfTheEventDate.year, month=t.tasckStartOfTheEventDate.month, day=t.tasckStartOfTheEventDate.day+1)
                        except ValueError:
                            try:
                                t.tasckStartOfTheEventTime = time(hour=t.tasckStartOfTheEventTime.hour + int(t.tasckPeriodical.split()[0].split(":")[0]) - 24, minute=t.tasckStartOfTheEventTime.minute, second=t.tasckStartOfTheEventTime.second)
                                t.tasckStartOfTheEventDate = date(year=t.tasckStartOfTheEventDate.year, month=t.tasckStartOfTheEventDate.month+1, day=t.tasckStartOfTheEventDate.day+1-(calendar.monthrange(t.tasckStartOfTheEventDate.year, month=t.tasckStartOfTheEventDate.month+1)[1]))
                            except ValueError:
                                t.tasckStartOfTheEventTime = time(hour=t.tasckStartOfTheEventTime.hour + int(t.tasckPeriodical.split()[0].split(":")[0]) - 24, minute=t.tasckStartOfTheEventTime.minute, second=t.tasckStartOfTheEventTime.second)
                                t.tasckStartOfTheEventDate = date(year=t.tasckStartOfTheEventDate.year+1, month=t.tasckStartOfTheEventDate.month+1-12, day=t.tasckStartOfTheEventDate.day+1-(calendar.monthrange(t.tasckStartOfTheEventDate.year, month=t.tasckStartOfTheEventDate.month+1)[1]))
            if t.tasckStatus:
                m -=1
                t.tasckStatus = False
            t.save()
    data = {
        "form": form,
        "tascks": Tasck.objects.all().filter(tasckStatusPeriodical=False).order_by('-tasckId'),
        "periodicalTasks": periodicalTasks.order_by('-tasckId'),
        "n": len(Tasck.objects.all().filter(tasckStatus=False, tasckStatusPeriodical=False, isDelate=False)),
        "m": m,
        "p": len(periodicalTasks),
    }
    return render(request, 'taskmanager/index.html', data)

def form(request):
    form = TasckForm
    if request.method == 'POST':
        form = TasckForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            TasckForm()
    data = {
        "form": form,
    }
    return render(request, 'taskmanager/form.html', data)

def edit(request, id):
    form = TasckForm(request.POST)
    data = {
        "form": form,
        "tascks": Tasck.objects.all()
    }
    try:
        task = Tasck.objects.get(id=id)
        if request.method == "POST":
            task.tasckStatus = bool(request.POST.get("tasckStatus"))
            task.isDelate = bool(request.POST.get("isDelate"))
            task.save()
            return redirect('index')
        else:
            return render(request, "taskmanager/index.html", data)
    except Tasck.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")

def edit_task(request, id):
    form = TasckForm(instance=Tasck.objects.get(id=id))
    data = {
        "form": form,
        "tascks": Tasck.objects.get(id=id),
    }
    try:
        task = Tasck.objects.get(id=id)
        if request.method == "POST":
            form = TasckForm(request.POST)
            if form.is_valid():
                task.tasckTitle = request.POST.get("tasckTitle")
                task.tasckDescription = request.POST.get("tasckDescription")
                task.tasckStartOfTheEventDate = date(
                    day=int(str(request.POST.get("tasckStartOfTheEventDate")).split(".")[0]),
                    month=int(str(request.POST.get("tasckStartOfTheEventDate")).split(".")[1]),
                    year=int(str(request.POST.get("tasckStartOfTheEventDate")).split(".")[2])
                )
                task.tasckStartOfTheEventTime = time(
                    hour=int(str(request.POST.get("tasckStartOfTheEventTime")).split(":")[0]),
                    minute=int(str(request.POST.get("tasckStartOfTheEventTime")).split(":")[1]),
                    second=int(str(request.POST.get("tasckStartOfTheEventTime")).split(":")[2])
                )
                task.tasckDuration = timedelta(
                    hours=int(str(request.POST.get("tasckDuration")).split(":")[0]),
                    minutes=int(str(request.POST.get("tasckDuration")).split(":")[1]),
                    seconds=int(str(request.POST.get("tasckDuration")).split(":")[2])
                )
                task.tasckPlace = request.POST.get("tasckPlace")
                task.tasckTravelTime = timedelta(
                    hours=int(str(request.POST.get("tasckTravelTime")).split(":")[0]),
                    minutes=int(str(request.POST.get("tasckTravelTime")).split(":")[1]),
                    seconds=int(str(request.POST.get("tasckTravelTime")).split(":")[2])
                )
                task.tasckStatusPeriodical = bool(request.POST.get("tasckStatusPeriodical"))
                tasckPeriodical = str(request.POST.get("tasckPeriodical"))
                tasckPeriodical = tasckPeriodical.split()
                if len(tasckPeriodical) > 1 and tasckPeriodical[0] != 'None':
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
                            tmp = int(tasckPeriodical[0])
                            for i in tasckPeriodical[-1].split(":"):
                                tmp = int(i)
                        except ValueError:
                            task.tasckPeriodical = None
                            task.tasckId = request.POST.get("tasckId")
                            task.save()
                task.tasckPeriodical = ""
                tasckPeriodical = list(str(tasckPeriodical))
                i = 0
                c = len(tasckPeriodical)
                while i < c:
                    if not tasckPeriodical[i].isdigit():
                        if not(tasckPeriodical[i] in " day, :"):
                            tasckPeriodical.pop(i)
                            c -= 1
                            i = 0
                    i += 1
                for j in tasckPeriodical:
                    task.tasckPeriodical += j
                if task.tasckPeriodical[0].isdigit():
                    task.tasckPeriodical = task.tasckPeriodical
                else:
                    task.tasckPeriodical = task.tasckPeriodical[1:]
                task.tasckId = request.POST.get("tasckId")
                task.save()
                return redirect('index')
            else:
                TasckForm()
                data = {
                    "form": form,
                    "tascks": Tasck.objects.get(id=id),
                }
                return render(request, "taskmanager/form_edit.html", data)
    except Tasck.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")
    return render(request, "taskmanager/form_edit.html", data)

class CalendarView(generic.ListView):
    model = Tasck

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('day', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
