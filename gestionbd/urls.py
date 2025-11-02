from django.urls import path, re_path

from . import views

app_name = 'gestionbd'
urlpatterns = [
    re_path(r'^$', views.index, name="index"),
   
    path(r'ver/<int:id>', views.ver_modulo, name="ver"),
   
    path("editar_textos_ras/<int:idmodulo>", views.editar_criterios_aprendizaje, name="editar_criterios_aprendizaje"),
    
    path("mostrar_ras_dualizar/<int:idmodulo>", views.mostrar_ras_dualizar, name="mostrar_ras_dualizar"),
    path("dualizar_criterios_individuales/<int:idra>", views.dualizar_criterios_individuales, name="dualizar_criterios_individuales"),
    path("activar_dualizacion_todo_ra/<int:idra>", views.activar_dualizacion_todo_ra, name="activar_dualizacion_todo_ra"),
    path("desactivar_dualizacion_todo_ra/<int:idra>", views.desactivar_dualizacion_todo_ra, name="desactivar_dualizacion_todo_ra"),
    
]