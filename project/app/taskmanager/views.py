from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .forms import TasckForm
from .models import Tasck
from django.http import HttpResponseNotFound
from datetime import date, time, timedelta

def index(request):
    form = TasckForm
    data = {
        "form": form,
        "tascks": Tasck.objects.all()
    }
    return render(request, 'taskmanager/index.html', data)
def form(request):
    error = ""
    if request.method == 'POST':
        form = TasckForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            form.add_error(None, "Ваша задача накладывается на другую задачу")
            error = "Ошибка валидации, проверьте, правильно ли вы заполнили все поля, скорее всего ваша задача накладывается на другую задачу"
    form = TasckForm
    data ={
        "form": form,
        "error": error
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
            task.save()
            return redirect('index')
        else:
            return render(request, "taskmanager/index.html", data)
    except Tasck.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")
def edit_task(request, id):
    form = TasckForm(instance=Tasck.objects.get(id=id))
    error = ""
    data = {
        "form": form,
        "tascks": Tasck.objects.get(id=id),
        "error": error
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
                if task.tasckPeriodical != None:
                    task.tasckPeriodical = request.POST.get("tasckPeriodical")
                task.save()
                return redirect('index')
            else:
                error = "Ошибка валидации, проверьте, правильно ли вы заполнили все поля, скорее всего ваша задача накладывается на другую задачу, в связи с чем система отменила изминение задачи"
                data = {
                    "form": form,
                    "tascks": Tasck.objects.get(id=id),
                    "error": error
                }
                return render(request, "taskmanager/form_edit.html", data)
    except Tasck.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")
    return render(request, "taskmanager/form_edit.html", data)
