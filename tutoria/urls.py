#!/usr/bin/env python3
from django.conf.urls import url

from . import views
app_name = 'tutoria'
urlpatterns = [
    url(r'^$', views.index_tutoria, name="index"),
    url(r'^anadir$', views.anadir, name="anadir"),
    url(r'^editar/(?P<id>[A-Z0-9]+)$', views.editar, name="editar"),
    url(r'^index_matricula$', views.index_matricula, name="index_matricula"),
    url(r'^realizar_matricula/(?P<modulo>[0-9]+)$',
        views.realizar_matricula,
        name="realizar_matricula"),
    url(r'^emails/(?P<nombre_curso>[A-Za-z_0-9]+)$', views.get_emails, name="get_emails"),
    url(r'^listas_alumnos_grupos$', views.get_listas_alumnos, name="listas_alumnos_grupos"),
    url(r'^lista_alumnos_por_grupo/(?P<grupo>[A-Za-z_0-9]+)$',
        views.get_lista_alumnos_por_grupo, name="lista_alumnos_por_grupo"),
]