from django.urls import path, re_path

from . import views

app_name = 'gestionbd'
urlpatterns = [
    re_path(r'^$', views.index, name="index"),
    re_path(r'^cortar$', views.cortar_elementos, name="cortar"),
    re_path(r'^index$', views.index, name="index"),
    re_path(r'^ver/([0-9]+)$', views.ver_modulo, name="ver"),
    re_path(r'^get_json_ciclos$', views.get_json_ciclos, name="get_json_ciclos"),
    re_path(r'^get_json_modulos/([0-9]+)$', views.get_json_modulo, name="get_json_modulos"),
    re_path(r'^get_json_ras/([0-9]+)$', views.get_json_ras, name="get_json_ras")
]