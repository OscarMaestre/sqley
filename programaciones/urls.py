from django.urls import path, re_path

from . import views

app_name = 'programaciones'
urlpatterns = [
    re_path(r'^index$', views.index, name="index"),
    re_path(r'^$', views.index, name="index"),
    re_path(r'^crear$', views.crear, name="crear"),
    re_path(r'^crear_ut/([0-9]+)?$', views.crear_ut, name="crear_ut"),
    re_path(r'^asignar_criterios/([0-9]+)?$', views.asignar_criterios, name="asignar_criterios"),
    re_path(r'^editar/([0-9])+/$', views.editar, name="editar"),
    re_path(r'^editar_objetivos_generales/(\d)+/$',
        views.editar_objetivos_generales, name="editar_objetivos_generales"),
]