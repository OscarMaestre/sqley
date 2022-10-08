#!/usr/bin/env python3
from django.urls import path

from . import views
app_name = 'tutoria'
urlpatterns = [
    path(r'^$', views.index_tutoria, name="index"),
    path(r'^anadir$', views.anadir, name="anadir"),
    path(r'^editar/(?P<id>[A-Z0-9]+)$', views.editar, name="editar"),
    path(r'^index_matricula$', views.index_matricula, name="index_matricula"),
    path(r'^realizar_matricula/(?P<modulo>[0-9]+)$',
        views.realizar_matricula,
        name="realizar_matricula"),
    path(r'^emails/(?P<nombre_curso>[A-Za-z_0-9]+)$', views.get_emails, name="get_emails"),
    path(r'^listas_alumnos_grupos$', views.get_listas_alumnos, name="listas_alumnos_grupos"),
    path(r'^lista_alumnos_por_grupo/(?P<grupo>[A-Za-z_0-9]+)$',
        views.get_lista_alumnos_por_grupo, name="lista_alumnos_por_grupo"),
]