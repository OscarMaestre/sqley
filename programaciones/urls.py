from django.conf.urls import url

from . import views

app_name = 'programaciones'
urlpatterns = [
    url(r'^index$', views.index, name="index"),
    url(r'^$', views.index, name="index"),
    url(r'^crear$', views.crear, name="crear"),
    url(r'^editar/([0-9])+/$', views.editar, name="editar"),
    url(r'^editar_objetivos_generales/(\d)+/$',
        views.editar_objetivos_generales, name="editar_objetivos_generales"),
]