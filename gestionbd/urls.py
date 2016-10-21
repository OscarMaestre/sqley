from django.conf.urls import url

from . import views

app_name = 'gestionbd'
urlpatterns = [
    url(r'^cortar$', views.cortar_elementos, name="index"),
    
]