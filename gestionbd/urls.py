from django.conf.urls import url

from . import views

app_name = 'gestionbd'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^cortar$', views.cortar_elementos, name="cortar"),
    url(r'^index$', views.index, name="index"),
    url(r'^ver/([0-9]+)$', views.ver_modulo, name="ver"),
    url(r'^get_json_ciclos$', views.get_json_ciclos, name="get_json_ciclos"),
    url(r'^get_json_modulos/([0-9]+)$', views.get_json_modulo, name="get_json_modulos"),
    url(r'^get_json_ras/([0-9]+)$', views.get_json_ras, name="get_json_ras")
]