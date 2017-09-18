#!/usr/bin/env python3
# coding=utf-8
import yaml, sys, re
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("ciclos")
configurador.activar_configuracion ("ciclos.settings")
from gestionbd.models import *
from django.db import transaction
#Poner a True para no hacer el guardado en la BD
#y así ir mas deprisa
#DEBUG=True
DEBUG=False
PATRON_NO_ENCONTRADO="xXxXxXxX"

re_letra_con_parentesis="[a-zñ]\)"
expr_regular_letra_con_parentesis=re.compile ( re_letra_con_parentesis )
re_num_con_punto="[0-9]{1,2}\."
expr_regular_num_con_punto = re.compile ( re_num_con_punto )

def extraer_ra(texto_ra):
    pos_punto=texto_ra.find(".")
    numero=texto_ra[0:pos_punto]
    texto_resultado=texto_ra[pos_punto+1:].strip()
    return (numero, texto_resultado)

def extraer_letra_y_parentesis(linea):
    print (">>>>>",linea)
    pos_letra=linea.find(")")
    letra=linea[0:pos_letra]
    texto_resultado=linea[pos_letra+1:].strip()
    return (letra, texto_resultado)

def extraer_datos_criterio ( texto_crit ):
    return extraer_letra_y_parentesis ( texto_crit )
    


def linea_contiene_patron(expr_regular, linea):
        """
        Dice si una linea contiene un patron
        
        Argumentos:
        
            expr_regular -- Expresión regular ya compilada
            
            linea -- línea en la que buscar el texto
            
        Devuelve:
        
            (inicio, fin, texto) -- Tupla con la posicion de inicio, la de final y el texto
            encontrado. Si no aparece nada se devuelve la constante ProcesadorPDF.PATRON_NO_ENCONTRADO
        
        """
        #print ("Buscando {0} en {1}".format( str(expr_regular), linea))
        concordancia=expr_regular.search(linea)
        if concordancia:
            inicio=concordancia.start()
            final=concordancia.end()
            patron=concordancia.string[inicio:final]
            #print ("-->Encontrado {0} en {1}".format( str(expr_regular), linea))
            return (inicio, final, patron)
        return (PATRON_NO_ENCONTRADO, PATRON_NO_ENCONTRADO, PATRON_NO_ENCONTRADO)
def extraer_identificador ( linea ):
    (ini, fin, texto)=linea_contiene_patron ( expr_regular_num_con_punto, linea)
    if texto==PATRON_NO_ENCONTRADO:
        return linea_contiene_patron ( expr_regular_letra_con_parentesis, linea)
    return (ini, fin, texto)


def crear_cualificacion(ciclo_asociado, cual, completa):
    codigo=cual["cualificacion"]["codigo"]
    rd = cual["cualificacion"]["real_decreto"]
    texto_cual = cual["cualificacion"]["texto"]
    print (codigo, rd, texto_cual)
    cualificacion = CualificacionProfesional(
        identificador=codigo,
        texto=texto_cual,
        real_decreto=rd
    )
    cualificacion.save()
    cualificacion_asociada=cualificacion
    ciclo_tiene_cualificacion=CicloTieneCualificacion.objects.create(
        ciclo=ciclo_asociado, cualificacion_profesional=cualificacion,
        es_completa=completa
    )
    ciclo_tiene_cualificacion.save()
    
    for u in cual["cualificacion"]["unidades_de_competencia"]:
        #print(u)
        cualificacion_asociada=cualificacion
        codigo = u["unidad"]["codigo"].strip()
        texto_competencia = u["unidad"]["texto"].strip()
        uc=UnidadDeCompetencia(
            identificador=codigo,
            texto=texto_competencia,
        )
        uc.save()
        uc.cualificacion.add(cualificacion_asociada)
        print(">>",codigo, texto_competencia)
        
def procesar_archivo():
    archivo_ciclo=open ( sys.argv[1], encoding="utf-8" )
    
    y=yaml.safe_load(archivo_ciclo)
    
    nombre_ciclo= y["ciclo"]["nombre"]
    
    nombre_pasado=sys.argv[2]
    if nombre_pasado=="DAM" or nombre_pasado=="DAW" or nombre_pasado=="ASIR" or nombre_pasado=="DAWE" or nombre_pasado=="SCI":
        nivel=3
    if nombre_pasado=="SMIR" or nombre_pasado=="SMIRE" or nombre_pasado=="MCOM":
        nivel=2
    if nombre_pasado=="FPB":
        nivel=1
    ciclo=Ciclo (nombre=nombre_ciclo, abreviatura=sys.argv[2],nivel_profesional=nivel)
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
        grupo_1_matinal=Grupo(nombre_grupo="MIF1-Tarde", curso=curso_1)
        grupo_2_matinal=Grupo(nombre_grupo="MIF2-Tarde", curso=curso_2)
        grupo_1_matinal.save()
        grupo_2_matinal.save()
    if sys.argv[2]=="SMIRE":
        grupo_1_elearning=Grupo(nombre_grupo="MIF1-Elearning", curso=curso_1)
        grupo_2_elearning=Grupo(nombre_grupo="MIF2-Elearning", curso=curso_2)
        grupo_1_elearning.save()
        grupo_2_elearning.save()
    if sys.argv[2]=="DAW":
        grupo_daw1_tarde=Grupo(nombre_grupo="DAW1-Tarde", curso=curso_1)
        grupo_daw2_tarde=Grupo(nombre_grupo="DAW2-Tarde", curso=curso_2)
        grupo_daw1_tarde.save()
        grupo_daw2_tarde.save()
    if sys.argv[2]=="DAWE":
        grupo_daw1_elearning=Grupo(nombre_grupo="DAW1-Elearning", curso=curso_1)
        grupo_daw2_elearning=Grupo(nombre_grupo="DAW2-Elearning", curso=curso_2)
        grupo_daw1_elearning.save()
        grupo_daw2_elearning.save()
        
    if sys.argv[2]=="MCOM":
        grupo1_mcom=Grupo(nombre_grupo="MCOM1", curso=curso_1)
        grupo2_mcom=Grupo(nombre_grupo="MCOM2", curso=curso_2)
        grupo1_mcom.save()
        grupo2_mcom.save()
    if sys.argv[2]=="SCI":
        grupo1_mcom=Grupo(nombre_grupo="SCI1", curso=curso_1)
        grupo2_mcom=Grupo(nombre_grupo="SCI2", curso=curso_2)
        grupo1_mcom.save()
        grupo2_mcom.save()
    
    competencia_general = y["ciclo"]["competencia_general"]
    comp_general = CompetenciaGeneral ( texto=competencia_general, ciclo=el_ciclo)
    comp_general.save()
    for c in y["ciclo"]["competencias"]:
        (ini_id, fin_id, id)=extraer_identificador(c)
        id=str(id)
        texto=c[fin_id+1:]
        texto_competencia=texto.strip()
        ciclo_asociado=ciclo
        competencia=Competencia(identificador=id, texto=texto_competencia, ciclo=ciclo_asociado)
        competencia.save()
    
    objetivos_generales = y["ciclo"]["objetivos_generales"]
    for o in objetivos_generales:
        (letra_obj, texto_obj) = extraer_letra_y_parentesis ( o )
        objetivo=ObjetivoGeneral ( letra=letra_obj, texto=texto_obj, ciclo=ciclo_asociado)
        objetivo.save()
            
    for cual in y["ciclo"]["cualificaciones_completas"]:
        crear_cualificacion(ciclo_asociado, cual, True)
    
    try:
        for cual in y["ciclo"]["cualificaciones_incompletas"]:
            crear_cualificacion(ciclo_asociado, cual, False)
    except:
        #Algunos ciclos no tiene cualificaciones incompletas
        pass
        
    
    for m in y["ciclo"]["modulos"]:
        nombre_modulo = m["modulo"]["nombre"]
        ciclo_aux=ciclo
        codigo=m["modulo"]["codigo"]
        
        horas_anio=m["modulo"]["duracion"]
        horas_semana=m["modulo"]["horas_semanales"]
        curso_de_imparticion=m["modulo"]["curso"]
        print (nombre_modulo, curso_de_imparticion, codigo)
        #sys.exit(-1)
        if curso_de_imparticion==1:
            curso_asociado=curso_1
            print ("Asociando con 1")
        else:curso_asociado=curso_2
            
        espe=m["modulo"]["especialidad"]
        modulo=Modulo ( nombre=nombre_modulo,
                       codigo_junta=str(codigo),
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
            print (r)
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