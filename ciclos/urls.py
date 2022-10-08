"""ciclos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  path(r'^blog/', include(blog_urls))
"""
from django.conf.urls import  include
from django.urls import path

from django.contrib import admin
from reparto import urls
from programaciones import urls
from gestionbd import urls
from tutoria import views as vistas_tutoria

urlpatterns = [
    path(r'^admin/', admin.site.urls),
    path(r'^reparto/', include('reparto.urls')),
    path(r'^programaciones/', include ('programaciones.urls')),
    path(r'^gestionbd/', include ('gestionbd.urls')),
    path(r'^alumnos/', include('tutoria.urls')),
    path(r'^$', vistas_tutoria.anadir)
]
