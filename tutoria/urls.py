#!/usr/bin/env python3
from django.urls import path,re_path

from . import views
app_name = 'tutoria'
urlpatterns = [
    re_path(r'^$', views.index_tutoria, name="index"),
    re_path(r'^anadir$', views.anadir, name="anadir"),
    re_path(r'^editar/(?P<id>[A-Z0-9]+)$', views.editar, name="editar"),
    re_path(r'^index_matricula$', views.index_matricula, name="index_matricula"),
    re_path(r'^realizar_matricula/(?P<modulo>[0-9]+)$',
        views.realizar_matricula,
        name="realizar_matricula"),
    re_path(r'^emails/(?P<nombre_curso>[A-Za-z_0-9]+)$', views.get_emails, name="get_emails"),
    re_path(r'^listas_alumnos_grupos$', views.get_listas_alumnos, name="listas_alumnos_grupos"),
    re_path(r'^lista_alumnos_por_grupo/(?P<grupo>[A-Za-z_0-9]+)$',
        views.get_lista_alumnos_por_grupo, name="lista_alumnos_por_grupo"),
]