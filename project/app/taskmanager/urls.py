from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("form/form.html", views.form, name="form"),
    path("<int:id>/", views.edit, name="edit"),
    path("form/<int:id>/form_edit.html", views.edit_task, name="edit_task"),
    path("calendar/calendar.html", views.CalendarView.as_view(), name='calendar'),
]
