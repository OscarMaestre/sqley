#!/usr/bin/env python3
from django.urls import path, re_path

from . import views
app_name = 'reparto'
urlpatterns = [
    re_path(r'^index$', views.index, name="index"),
    re_path(r'^asignar$', views.asignar_preferencias, name="asignar_preferencias"),
    re_path(r'^almacenar_preferencias/(?P<id_profesor>[0-9]+)/$',
        views.almacenar_preferencias, name="almacenar_preferencias"),
    re_path(r'^asignar_elearning/(?P<id_profesor>[0-9]+)/$',
        views.insertar_preferencias_todo_elearning, name="todoelearning"),
]