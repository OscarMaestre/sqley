#!/usr/bin/env python3

from .models import *
from django.template.loader import render_to_string
class GeneradorInformesReparto(object):
    @staticmethod
    def generar_informes():
        repartos=Reparto.objects.all()
        for reparto in repartos:
            contexto=dict()
            
            print ("Generando para :"+reparto.nombre)
            cadenas_reparto=GeneradorInformesReparto.generar_informe_reparto_unico(reparto)
            contexto["reparto"]=reparto
            contexto["repartos"]=cadenas_reparto
            print("Guardando...")
            descriptor=open(reparto.nombre+".html", "w", encoding="utf-8")
            descriptor.write(render_to_string("reparto/reparto.html", contexto))
            descriptor.flush()
            descriptor.close()
            print("Reparto escrito:"+reparto.nombre)
            
    @staticmethod
    def generar_informe_reparto_unico(objeto_reparto):
        profesores=Profesor.objects.all().order_by("num_posicion")
        cadenas=[]
        for prof in profesores:
            asignaciones=Asignacion.objects.filter(reparto=objeto_reparto,
                                               profesor=prof)
            modulos_asociados=[]
            horas_asignadas=0
            for a in asignaciones:
                modulos_asociados.append(a.modulo)
                horas_asignadas+=a.modulo.horas_semanales
            contexto=dict()
            contexto["profesor"]=prof
            contexto["modulos"]=modulos_asociados
            contexto["horas_asignadas"]=horas_asignadas
            cad_devolver=render_to_string("reparto/horario_personal.html", contexto)
            cadenas.append(cad_devolver)
        return cadenas
            