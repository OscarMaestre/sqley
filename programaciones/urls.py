from django.urls import path

from . import views

app_name = 'programaciones'
urlpatterns = [
    path(r'^index$', views.index, name="index"),
    path(r'^$', views.index, name="index"),
    path(r'^crear$', views.crear, name="crear"),
    path(r'^crear_ut/([0-9]+)?$', views.crear_ut, name="crear_ut"),
    path(r'^asignar_criterios/([0-9]+)?$', views.asignar_criterios, name="asignar_criterios"),
    path(r'^editar/([0-9])+/$', views.editar, name="editar"),
    path(r'^editar_objetivos_generales/(\d)+/$',
        views.editar_objetivos_generales, name="editar_objetivos_generales"),
]