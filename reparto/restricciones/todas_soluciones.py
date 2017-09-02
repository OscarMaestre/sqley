#!/usr/bin/env python3

import os
from Configurador import Configurador
configurador=Configurador(".." + os.sep + "..")
configurador.activar_configuracion("ciclos.settings")
from gestionbd.models import Profesor, Modulo, EspecialidadProfesor, Grupo
from reparto.models import ModuloEnReparto
from django.db.models import Q

from constraint import *
from itertools import combinations_with_replacement


#Modulos que se pueden repartir en secundaria
def get_modulos(con_ordenacion=False):
        filtro_modulos_ps=Q(especialidad="PS")
        filtro_modulos_todos=Q(especialidad="TODOS")
        filtro_horas=Q(horas_semanales__gt=0)
        filter_general=filtro_horas & (filtro_modulos_ps | filtro_modulos_todos )
        lista_modulos=[]
        grupos=Grupo.objects.all()
        num_para_anadir_un_codigo=1
        for g in grupos:
            curso_asociado=g.curso
            #print(curso_asociado)
            if con_ordenacion:
                modulos_asociados=Modulo.objects.filter(
                    curso=curso_asociado).filter(
                    filter_general).order_by("-horas_semanales", "nombre")
            else:
                modulos_asociados=Modulo.objects.filter(curso=curso_asociado).filter(filter_general)
            #print(modulos_asociados)
            
            for m in modulos_asociados:
                modulo_para_repartir=ModuloEnReparto(modulo_asociado=m,
                                                     grupo_asociado=g)
                modulo_para_repartir.codigo_r=num_para_anadir_un_codigo
                num_para_anadir_un_codigo+=1
                print(num_para_anadir_un_codigo)
                lista_modulos.append(modulo_para_repartir)
        return lista_modulos

problema = Problem()


esp_ps      =   EspecialidadProfesor.objects.filter(especialidad="PS")
profesores  =   Profesor.objects.filter(especialidad=esp_ps).order_by("num_posicion")
modulos     =   get_modulos()

#print (profesores)
#print(modulos)
profesores=[1, 2, 3]
modulos=[4,4,4,4,4,4,4]
combinaciones = combinations_with_replacement(profesores, len(modulos))

for c in combinaciones:
        print (c)