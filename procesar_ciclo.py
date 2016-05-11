#!/usr/bin/env python3
#coding=utf-8
from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
import sys, re


re_resultado_aprendizaje="de aprendizaje y criterios"
expr_regular_resultado_aprendizaje=re.compile ( re_resultado_aprendizaje )

re_resultado="^[0-9]\."
expr_regular_resultado=re.compile ( re_resultado )

COMIENZOS_MODULOS=["Módulo Profesional: " , "Módulo profesional: "]
COMIENZO_CODIGO="Código: "
DURACION="Duración:"
MODO_LEYENDO_CRITERIOS=1
MODO_ESPERANDO_CONTENIDOS=2

def extraer_resto_linea(linea, comienzo):
    pos_comienzo_resto=len(comienzo)
    resto=linea_actual[pos_comienzo_resto:].strip()
    return resto

def extraer_nombre_modulo(linea):
    for comienzo in COMIENZOS_MODULOS:
        if comienzo in linea:
            return extraer_resto_linea(linea, comienzo)
    return False    
        
procesador=ProcesadorPDF()
procesador.abrir_fichero_txt ( sys.argv[1] )

linea_actual=procesador.get_linea_actual()
modo=0
while not procesador.eof():

    posible_nombre_modulo=extraer_nombre_modulo(linea_actual)
    if posible_nombre_modulo:
        print (posible_nombre_modulo)
    
    if COMIENZO_CODIGO in linea_actual:
        pos_comienzo_codigo=len(COMIENZO_CODIGO)
        codigo=linea_actual[pos_comienzo_codigo:].strip()
        print (codigo)
        (ini, fin, result)=procesador.avanzar_buscando_patron (
            expr_regular_resultado_aprendizaje )
    
    if re_resultado_aprendizaje in linea_actual:
        procesador.siguiente_linea()
        linea_actual=procesador.get_linea_actual()
        modo=MODO_LEYENDO_CRITERIOS
        
    if DURACION in linea_actual:
        horas=extraer_resto_linea ( linea_actual, DURACION )
        horas=horas[2:].replace(" horas", "")
        print (horas)
        
    if MODO_LEYENDO_CRITERIOS and "Duración" in linea_actual:
        modo=MODO_ESPERANDO_CONTENIDOS
    procesador.siguiente_linea()
    linea_actual=procesador.get_linea_actual()