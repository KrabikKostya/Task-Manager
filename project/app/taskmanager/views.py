from datetime import datetime
from .utils import Calendar
from .models import *
from django.utils.safestring import mark_safe
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render
from datetime import date, timedelta, time
from django.shortcuts import render, redirect
from .forms import TasckForm
from .models import Tasck
from django.http import HttpResponseNotFound


def index(request):
    form = TasckForm
    data = {
        "form": form,
        "tascks": Tasck.objects.all().order_by('-tasckId'),
        "n": len(Tasck.objects.all().filter(tasckStatus=False)),
        "m": len(Tasck.objects.all().filter(tasckStatus=True)),
        "d": len(Tasck.objects.all().filter(isDelate=True)),
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
    data ={
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
                    month = int(str(request.POST.get("tasckStartOfTheEventDate")).split(".")[1]),
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
                if task.tasckPeriodical != None and task.tasckStatusPeriodical:
                    task.tasckPeriodical = request.POST.get("tasckPeriodical")
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


# def calendar(request):
#     data = {
#         "form": form,
#         "tascks": Tasck.objects.all()
#     }
#     return render(request, 'taskmanager/calendar.html', data)


class CalendarView(generic.ListView):
    model = Tasck
    # template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
