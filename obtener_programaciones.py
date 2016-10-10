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
from math import ceil


def get_objetivos(modulo_pasado):
    objetivos=ObjetivosModulo.objects.filter(modulo=modulo_pasado)
    
    return (objetivos[0].objetivos.all())
    
    
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
        diccionario["nombre_profesor"]=autor
        diccionario["horas_semanales_modulo"]=modulo.horas_semanales
        diccionario["horas_anuales_modulo"]=modulo.horas_anuales
        horas_perdida_evaluacion = ceil ( modulo.horas_anuales * 0.2 )
        diccionario["horas_perdida_evaluacion"] = horas_perdida_evaluacion
        diccionario["objetivos_generales_modulo"] = get_objetivos ( modulo )
        print (diccionario["objetivos_generales_modulo"])
        c_general=modulo.curso.ciclo.competenciageneral_set.all()
        print (c_general[0])
        diccionario["competencia_general_ciclo"]=c_general[0]
        nombre_fichero_programacion = NOMBRE_FICHERO.format(nombre_grupo, nombre_modulo, autor)
        fichero=open(nombre_fichero_programacion, "w")
        resultado=render_to_string("programaciones/plantilla_programacion.html", diccionario)
        fichero.write(resultado)
        fichero.close()
    