#!/usr/bin/env python3
from django.urls import path

from . import views
app_name = 'reparto'
urlpatterns = [
    path(r'^index$', views.index, name="index"),
    path(r'^asignar$', views.asignar_preferencias, name="asignar_preferencias"),
    path(r'^almacenar_preferencias/(?P<id_profesor>[0-9]+)/$',
        views.almacenar_preferencias, name="almacenar_preferencias"),
    path(r'^asignar_elearning/(?P<id_profesor>[0-9]+)/$',
        views.insertar_preferencias_todo_elearning, name="todoelearning"),
]