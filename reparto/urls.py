#!/usr/bin/env python3
from django.conf.urls import url

from . import views

app_name = 'reparto'
urlpatterns = [
    url(r'^index$', views.index, name="index"),
]