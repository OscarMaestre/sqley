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

def cargar_metodologias():
    lineas_metodologias=gf.get_lineas_fichero("datos_iniciales" + os.sep +"metodologias.txt")
    for l in lineas_metodologias:
        m=PuntoMetodologico(
            texto=l
        )
        m.save()

with transaction.atomic():
    PuntoMetodologico.objects.all().delete()
    cargar_metodologias()
    ev1=Evaluacion(numero=1, fecha_inicio="2016-09-18", fecha_fin="2016-12-20")
    ev1.save()
    ev2=Evaluacion(numero=2, fecha_inicio="2017-01-10", fecha_fin="2017-03-20")
    ev2.save()
    ev3=Evaluacion(numero=3, fecha_inicio="2017-04-01", fecha_fin="2017-06-20")
    ev3.save()