from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("form/form.html", views.form, name="form"),
    path("<int:id>/", views.edit, name="edit"),
    path("form/<int:id>/form_edit.html", views.edit_task, name="edit_task"),
    path("calendar/calendar.html", views.calendar, name="calendar"),
]
