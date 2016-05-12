#!/usr/bin/env python3
#coding=utf-8

from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
from utilidades.ficheros.GestorFicheros import GestorFicheros
import platform, glob
procesador=ProcesadorPDF()
gf=GestorFicheros()

lineas_borrado=gf.get_lineas_fichero ( "borrar.sql" )
for l in lineas_borrado:
    gf.enviar_texto_a_comando ( l, "sqlite3 ciclos.db")
    
ficheros_pdf=glob.glob("*.pdf")

for f in ficheros_pdf:
    procesador.convertir_a_txt(f)


if platform.system()=="Windows":
    gf.ejecutar_comando ( "ciclo.py", "daw.yaml", "DAW")
else:
    gf.ejecutar_comando ( "./ciclo.py", "daw.yaml", "DAW")