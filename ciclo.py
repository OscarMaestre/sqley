#!/usr/bin/env python3
# coding=utf-8
import yaml, sys
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("ciclos")
configurador.activar_configuracion ("ciclos.settings")
from gestionbd.models import *

#Poner a True para no hacer el guardado en la BD
#y así ir mas deprisa
#DEBUG=True
DEBUG=False

def extraer_ra(texto_ra):
    pos_punto=texto_ra.find(".")
    numero=texto_ra[0:pos_punto]
    texto_resultado=texto_ra[pos_punto+1:].strip()
    return (numero, texto_resultado)

def extraer_datos_criterio ( texto_crit ):
    print (">>>>>",texto_crit)
    pos_letra=texto_crit.find(")")
    letra=texto_crit[0:pos_letra]
    texto_resultado=texto_crit[pos_letra+1:].strip()
    return (letra, texto_resultado)

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
    curso_de_imparticion=m["modulo"]["curso"]
    espe=m["modulo"]["especialidad"]
    modulo=Modulo ( nombre=nombre_modulo,
                   codigo_junta=codigo,
                   horas_anuales=horas_anio,
                   horas_semanales=horas_semana,
                   ciclo=ciclo_aux, curso = curso_de_imparticion,
                   especialidad=espe)
    modulo.save()
    modulo_aux=modulo
    print (nombre_modulo)
    print("###########################")
    resultados_aprendizaje=m["modulo"]["resultados"]
    indice=0
    for r in resultados_aprendizaje:
        texto_ra=list(r.keys())[0]
        
        (numero_resultado, texto_resultado)=extraer_ra(texto_ra)
        print ("\t",numero_resultado,"-", texto_resultado)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxx")
        ra=ResultadoDeAprendizaje (
            texto=texto_resultado,
            numero=int(numero_resultado),
            modulo=modulo_aux
        )
        if DEBUG==False:
            ra.save()
        for crit in m["modulo"]["resultados"][indice][texto_ra]:
            (letra_crit, texto_crit)=extraer_datos_criterio ( crit )
            criterio=CriterioDeEvaluacion (
                texto=texto_crit,
                letra=letra_crit,
                resultado_de_aprendizaje=ra
            )
            if DEBUG==False:
                criterio.save()
            print ("\t\t",letra_crit, "-", texto_crit)
            print("-------------------------")
        indice=indice+1
        
    print("********************")
    contenidos=m["modulo"]["contenidos"]
    indice=0
    for c in contenidos:
        texto_cont=list ( c.keys())[0]
        (numero_cont, texto_contenido)=extraer_ra ( texto_cont )
        contenido_a_salvar=Contenido (
            texto=texto_contenido,
            numero=numero_cont,
            modulo=modulo_aux
        )
        if DEBUG==False:
            contenido_a_salvar.save()
        print ("\t", numero_cont, "-", texto_contenido)
        textos_contenidos=m["modulo"]["contenidos"][indice]
        clave = list(textos_contenidos.keys())[0]
        #print (clave)
        #sys.exit()
        num_punto=1
        for punto_cont in textos_contenidos[clave]:
            #texto_punto_contenido=m["modulo"]["contenidos"]
            punto_contenido=PuntoDeContenido(
                texto=punto_cont,
                num_orden=num_punto,
                contenido=contenido_a_salvar
            )
            if DEBUG==False:
                punto_contenido.save()
            print("\t\t", num_punto, "-", punto_cont)
            num_punto=num_punto+1
        indice=indice+1
    
    #Fin del for
#print (y["ciclo"]["modulos"][1]["modulo"]["resultados"][1])


archivo_ciclo.close()