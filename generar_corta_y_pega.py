#!/usr/bin/env python3
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("ciclos")
configurador.activar_configuracion ("ciclos.settings")

from gestionbd.models import Modulo, Profesor, Ciclo, Competencia, CompetenciaGeneral, Contenido, ResultadoDeAprendizaje, PuntoDeContenido, ObjetivoGeneral, CriterioDeEvaluacion
from django.db.models.expressions import Q
from django.template.loader import render_to_string
import sys, os

DIRECTORIO_RESULTADOS   =   "para_cortar_y_pegar"
def generar_fichero_corta_y_pega ( codigo_modulo_segun_jccm, directorio_fichero_resultado):
    modulos = Modulo.objects.filter ( codigo_junta = codigo_modulo_segun_jccm ) #Importante, solo debe haber un resultado
    
    if len ( modulos ) == 0:
        print ("No hay ningun modulo cuyo campo codigo_junta sea " + codigo_modulo_segun_jccm)
        sys.exit(-1)
    if len(modulos)>1:
        print("Se encontraron varios modulos:"+str(len(modulos)))
        print(codigo_modulo_segun_jccm)
        print(modulos)
        
    for objeto_modulo in modulos:
        
        #Importante, solo debe haber un resultado
        #print (objeto_modulo[0])
        curso_asociado_al_modulo    =   objeto_modulo.curso
        ciclo_asociado              =   curso_asociado_al_modulo.ciclo
        #print (ciclo_asociado)
        
        print ("Procesando modulo "+objeto_modulo.nombre+" asociado al ciclo "+ ciclo_asociado.abreviatura)
        objetivos_generales_del_ciclo   =   ObjetivoGeneral.objects.filter ( ciclo = ciclo_asociado )
        
        resultados_de_aprendizaje       =   ResultadoDeAprendizaje.objects.filter ( modulo = objeto_modulo )
        
        criterios_de_evaluacion         =   CriterioDeEvaluacion.objects.filter(resultado_de_aprendizaje__modulo=objeto_modulo)
        
        competencias                    =   Competencia.objects.filter(ciclo=ciclo_asociado)
        
        cualificaciones                 =   ciclo_asociado.ciclotienecualificacion_set.all()
        #print(cualificaciones)
        #print (criterios_de_evaluacion)
        
        #print (objetivos_generales_del_ciclo)
        
        #Se genera el fichero
        
        nombre_fichero=objeto_modulo.nombre.replace(" ", "_")
        nombre_fichero=nombre_fichero.strip(".")
        nombre_fichero=nombre_fichero+"_"+ciclo_asociado.abreviatura+".html"
        #Debido a que el nombre del modulo a veces lleva un punto al final podría haber nombre como "modulo..html"
        #Asi que quitamos el ..
        nombre_fichero = nombre_fichero.replace("..", ".")
        
        
        nombre_fichero = directorio_fichero_resultado + os.sep + nombre_fichero 
        
        diccionario=dict()
        diccionario["objetivos_generales"]          =       objetivos_generales_del_ciclo
        diccionario["nombre_modulo"]                =       objeto_modulo.nombre
        diccionario["resultados_aprendizaje"]       =       resultados_de_aprendizaje
        diccionario["competencias"]                 =       competencias
        diccionario["cualificaciones"]              =       cualificaciones
        contenido_fichero = render_to_string("programaciones/para_cortar_y_pegar.html", diccionario)
        with open(nombre_fichero, "w", encoding="utf-8") as fichero:
            fichero.write(contenido_fichero)


if __name__ == '__main__':
    try:
        modulos=Modulo.objects.all().distinct()
        for m in modulos:
            codigo_modulo_segun_jccm=m.codigo_junta
            generar_fichero_corta_y_pega ( codigo_modulo_segun_jccm, DIRECTORIO_RESULTADOS )
        
        
    except Exception as e:
        print ("Tienes que suministrar el codigo de la Junta y se generará un HTML con todo listo para cortar y pegar")
        print(e)
        sys.exit(-1)
    
    



