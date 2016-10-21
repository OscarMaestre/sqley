from django.conf.urls import url

from . import views

app_name = 'gestionbd'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^cortar$', views.cortar_elementos, name="cortar"),
    url(r'^index$', views.index, name="index"),
    url(r'^ver/([0-9]+)$', views.ver_modulo, name="ver"),
    
]