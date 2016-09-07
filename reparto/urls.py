#!/usr/bin/env python3
from django.conf.urls import url

from . import views

app_name = 'reparto'
urlpatterns = [
    url(r'^index$', views.index, name="index"),
    url(r'^crear$', views.crear, name="crear"),
    url(r'^elegir/(?P<num_reparto>[0-9]*)$', views.elegir, name="elegir")
]