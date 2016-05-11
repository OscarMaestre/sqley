#!/usr/bin/env python
#coding=utf-8
from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
import sys

COMIENZOS_MODULOS=["Módulo Profesional:" , "Módulo profesional: "]
COMIENZO_CODIGO="Código:"



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
while not procesador.eof():

    posible_nombre_modulo=extraer_nombre_modulo(linea_actual)
    if posible_nombre_modulo:
        print (posible_nombre_modulo)
    
    #if COMIENZO_CODIGO in linea_actual:
    #    pos_comienzo_codigo=len(COMIENZO_CODIGO)
    #    codigo=linea_actual[pos_comienzo_codigo:].strip()
    #    print (codigo)
    procesador.siguiente_linea()
    linea_actual=procesador.get_linea_actual()