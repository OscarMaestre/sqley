#!/usr/bin/env python3
from django.conf.urls import url

from . import views
app_name = 'reparto'
urlpatterns = [
    url(r'^index$', views.index, name="index"),
    url(r'^asignar$', views.asignar_preferencias, name="asignar_preferencias"),
    url(r'^almacenar_preferencias/(?P<id_profesor>[0-9]+)/$',
        views.almacenar_preferencias, name="almacenar_preferencias"),
]