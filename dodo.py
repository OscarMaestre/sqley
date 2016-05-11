#!/usr/bin/env python
#coding=utf-8
from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
from utilidades.ficheros.GestorFicheros import GestorFicheros
import platform, glob

procesador=ProcesadorPDF()
gf=GestorFicheros()

ficheros_pdf=glob.glob("*.pdf")

for f in ficheros_pdf:
    procesador.convertir_a_txt(f)

ficheros_txt=glob.glob("*.txt")
for f in ficheros_txt:
    if platform.system()=="Windows":
        gf.ejecutar_comando ( "procesar_ciclo.py", f)
    else:
        gf.ejecutar_comando ( "./procesar_ciclo.py", f)