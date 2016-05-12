#!/usr/bin/env python3
# coding=utf-8
import yaml, sys
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("ciclos")
configurador.activar_configuracion ("ciclos.settings")
from gestionbd.models import *

def extraer_ra(texto_ra):
    pos_punto=texto_ra.find(".")
    numero=texto_ra[0:pos_punto]
    texto_resultado=texto_ra[pos_punto+1:].strip()
    return (numero, texto_resultado)


archivo_ciclo=open ( sys.argv[1], encoding="utf-8" )

y=yaml.safe_load(archivo_ciclo)

nombre_ciclo= y["ciclo"]["nombre"] 
ciclo=Ciclo (nombre=nombre_ciclo, abreviatura=sys.argv[2])
ciclo.save()

for m in y["ciclo"]["modulos"]:
    nombre_modulo = m["modulo"]["nombre"]
    ciclo_aux=ciclo
    codigo=m["modulo"]["codigo"]
    horas_anio=m["modulo"]["duracion"]
    horas_semana=m["modulo"]["horas_semanales"]
    modulo=Modulo ( nombre=nombre_modulo,
                   codigo_junta=codigo,
                   horas_anuales=horas_anio,
                   horas_semanales=horas_semana,
                   ciclo=ciclo_aux )
    modulo.save()
    modulo_aux=modulo
    resultados_aprendizaje=m["modulo"]["resultados"]
    for r in resultados_aprendizaje:
        texto_ra=list(r.keys())[0]
        
        (numero_resultado, texto_resultado)=extraer_ra(texto_ra)
        #print (numero_resultado,"-", texto_resultado)
        ra=ResultadoDeAprendizaje (
            texto=texto_resultado,
            numero=int(numero_resultado),
            modulo=modulo_aux
        )
        ra.save()
    print("********************")
#print (y["ciclo"]["modulos"][1]["modulo"]["resultados"][1])


archivo_ciclo.close()