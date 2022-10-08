from django.urls import path

from . import views

app_name = 'gestionbd'
urlpatterns = [
    path(r'^$', views.index, name="index"),
    path(r'^cortar$', views.cortar_elementos, name="cortar"),
    path(r'^index$', views.index, name="index"),
    path(r'^ver/([0-9]+)$', views.ver_modulo, name="ver"),
    path(r'^get_json_ciclos$', views.get_json_ciclos, name="get_json_ciclos"),
    path(r'^get_json_modulos/([0-9]+)$', views.get_json_modulo, name="get_json_modulos"),
    path(r'^get_json_ras/([0-9]+)$', views.get_json_ras, name="get_json_ras")
]