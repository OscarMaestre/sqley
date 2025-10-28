from django.urls import path, re_path

from . import views

app_name = 'gestionbd'
urlpatterns = [
    re_path(r'^$', views.index, name="index"),
   
    path(r'ver/<int:id>', views.ver_modulo, name="ver"),
   
    path("editar_criterios_aprendizaje/<int:idmodulo>", views.editar_criterios_aprendizaje, name="editar_criterios_aprendizaje")
]