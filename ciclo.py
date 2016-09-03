#!/usr/bin/env python3
# coding=utf-8
import yaml, sys
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("ciclos")
configurador.activar_configuracion ("ciclos.settings")
from gestionbd.models import *
from django.db import transaction
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

def procesar_archivo():
    archivo_ciclo=open ( sys.argv[1], encoding="utf-8" )
    
    y=yaml.safe_load(archivo_ciclo)
    
    nombre_ciclo= y["ciclo"]["nombre"] 
    ciclo=Ciclo (nombre=nombre_ciclo, abreviatura=sys.argv[2])
    ciclo.save()
    el_ciclo=ciclo
    curso_1=Curso( num_curso=1, nombre_curso=sys.argv[2]+"_1", ciclo=el_ciclo)
    curso_2=Curso( num_curso=2, nombre_curso=sys.argv[2]+"_2", ciclo=el_ciclo)
    curso_1.save()
    curso_2.save()
    
    if sys.argv[2]=="DAM":
        grupo_dam1_matinal=Grupo(nombre_grupo="DAM1-Matinal", curso=curso_1)
        grupo_dam2_matinal=Grupo(nombre_grupo="DAM2-Matinal", curso=curso_2)
        grupo_dam1_matinal.save()
        grupo_dam2_matinal.save()
    if sys.argv[2]=="FPB":
        grupo_1_matinal=Grupo(nombre_grupo="FPB1-Matinal", curso=curso_1)
        grupo_2_matinal=Grupo(nombre_grupo="FPB2-Matinal", curso=curso_2)
        grupo_1_matinal.save()
        grupo_2_matinal.save()
    if sys.argv[2]=="ASIR":
        grupo_1_matinal=Grupo(nombre_grupo="ASIR1-Matinal", curso=curso_1)
        grupo_2_matinal=Grupo(nombre_grupo="ASIR2-Matinal", curso=curso_2)
        grupo_1_matinal.save()
        grupo_2_matinal.save()
    if sys.argv[2]=="SMIR":
        grupo_1_matinal=Grupo(nombre_grupo="MIF1-Matinal", curso=curso_1)
        grupo_2_matinal=Grupo(nombre_grupo="MIF2-Matinal", curso=curso_2)
        grupo_1_matinal.save()
        grupo_2_matinal.save()
        grupo_1_matinal=Grupo(nombre_grupo="MIF1-tarde", curso=curso_1)
        grupo_2_matinal=Grupo(nombre_grupo="MIF2-tarde", curso=curso_2)
        grupo_1_matinal.save()
        grupo_2_matinal.save()
    if sys.argv[2]=="DAW":
        grupo_daw1_tarde=Grupo(nombre_grupo="DAW1-tarde", curso=curso_1)
        grupo_daw2_tarde=Grupo(nombre_grupo="DAW2-tarde", curso=curso_2)
        grupo_daw1_tarde.save()
        grupo_daw2_tarde.save()
    if sys.argv[2]=="DAWE":
        grupo_daw1_elearning=Grupo(nombre_grupo="DAW1-elearning", curso=curso_1)
        grupo_daw2_elearning=Grupo(nombre_grupo="DAW2-elearning", curso=curso_2)
        grupo_daw1_elearning.save()
        grupo_daw2_elearning.save()
    
    
    
    for m in y["ciclo"]["modulos"]:
        nombre_modulo = m["modulo"]["nombre"]
        ciclo_aux=ciclo
        codigo=m["modulo"]["codigo"]
        horas_anio=m["modulo"]["duracion"]
        horas_semana=m["modulo"]["horas_semanales"]
        curso_de_imparticion=m["modulo"]["curso"]
        print (nombre_modulo, curso_de_imparticion)
        if curso_de_imparticion==1:
            curso_asociado=curso_1
            print ("Asociando con 1")
        else:curso_asociado=curso_2
            
        espe=m["modulo"]["especialidad"]
        modulo=Modulo ( nombre=nombre_modulo,
                       codigo_junta=codigo,
                       horas_anuales=horas_anio,
                       horas_semanales=horas_semana,
                       curso = curso_asociado,
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
            #print ("\t", numero_cont, "-", texto_contenido)
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
                #print("\t\t", num_punto, "-", punto_cont)
                num_punto=num_punto+1
            indice=indice+1
        
        #Fin del for
    #print (y["ciclo"]["modulos"][1]["modulo"]["resultados"][1])
    
    
    archivo_ciclo.close()
    
with transaction.atomic():
    procesar_archivo()