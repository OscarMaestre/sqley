#!/usr/bin/python3

#!/usr/bin/env python3
# coding=utf-8

import os   
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("ciclos")
configurador.activar_configuracion ("ciclos.settings")
from programaciones.models import *
from gestionbd.models import *
from django.template.loader import render_to_string

progs=Programacion.objects.all()
NOMBRE_FICHERO="{0}-Programacion de {1} por {2}.html"
num_fichero=1
for p in progs:
    autor=p.profesor.nombre
    
    modulos=p.modulo.all()
    
    for modulo in modulos:
        diccionario=dict()
        nombre_ciclo_formativo=modulo.curso.ciclo.nombre
        nombre_grupo=modulo.curso.nombre_curso
        nombre_modulo=modulo.nombre
        print("Generando:",nombre_modulo, nombre_grupo)
        diccionario["nombre_ciclo_formativo"]=nombre_ciclo_formativo
        diccionario["nombre_modulo"]=nombre_modulo
        diccionario["nombre_grupo"]=nombre_grupo
        nombre_fichero_programacion = NOMBRE_FICHERO.format(nombre_grupo, nombre_modulo, autor)
        fichero=open(nombre_fichero_programacion, "w")
        resultado=render_to_string("programaciones/plantilla_programacion.html", diccionario)
        fichero.write(resultado)
        fichero.close()
    