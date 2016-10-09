#!/usr/bin/env python3
# coding=utf-8

import os   
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("ciclos")
configurador.activar_configuracion ("ciclos.settings")
from programaciones.models import *
from django.db import transaction

from utilidades.ficheros.GestorFicheros import GestorFicheros

gf=GestorFicheros()

DIR_DATOS_INICIALES = "datos_iniciales" + os.sep

def cargar_metodologias():
    lineas_metodologias=gf.get_lineas_fichero( DIR_DATOS_INICIALES +"metodologias.txt")
    for l in lineas_metodologias:
        m=PuntoMetodologico(
            texto=l
        )
        m.save()
    recursos=gf.get_lineas_fichero( DIR_DATOS_INICIALES + "recursos_didacticos.txt")
    for r in recursos:
        rec=RecursoDidactico ( nombre = r)
        rec.save()
    
    instrumentos_evaluacion = gf.get_lineas_fichero (DIR_DATOS_INICIALES + "mecanismos_evaluacion.txt")
    for instrumento in instrumentos_evaluacion:
        instru = InstrumentoEvaluacion ( nombre = instrumento )
        instru.save()
    
    procedimientos_evaluacion = gf.get_lineas_fichero ( DIR_DATOS_INICIALES + "procedimientos_evaluacion.txt")
    for p in procedimientos_evaluacion:
        proc  = ProcedimientoEvaluacion ( nombre = p )
        proc.save()
    
    calificadores = gf.get_lineas_fichero ( DIR_DATOS_INICIALES + "calificadores.txt")
    for c in calificadores:
        cali = Calificador ( texto = c)
        cali.save()

with transaction.atomic():
    PuntoMetodologico.objects.all().delete()
    RecursoDidactico.objects.all().delete()
    InstrumentoEvaluacion.objects.all().delete()
    ProcedimientoEvaluacion.objects.all().delete()
    cargar_metodologias()
    Evaluacion.objects.all().delete()
    ev1=Evaluacion(numero=1, fecha_inicio="2016-09-18", fecha_fin="2016-12-20")
    ev1.save()
    ev2=Evaluacion(numero=2, fecha_inicio="2017-01-10", fecha_fin="2017-03-20")
    ev2.save()
    ev3=Evaluacion(numero=3, fecha_inicio="2017-04-01", fecha_fin="2017-06-20")
    ev3.save()