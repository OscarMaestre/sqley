#!/usr/bin/env python3
#coding=utf-8


from utilidades.ficheros.GestorFicheros import GestorFicheros
import platform, glob

gf=GestorFicheros()

lineas_borrado=gf.get_lineas_fichero ( "borrar.sql" )
for l in lineas_borrado:
    gf.enviar_texto_a_comando ( l, "sqlite3 ciclos.db")
    

EXTRACCION_MODULOS="""
SELECT mod.id, mod.nombre, mod.horas_semanales, g.nombre_grupo, ciclos.nivel_profesional
    from ciclos, modulos as mod, grupos as g, cursos as cur
        where
            mod.curso_id=cur.id
        and
            especialidad<>'PT'
        and
            g.curso_id=cur.id
        and
            cur.ciclo_id=ciclos.id
        
    order by horas_semanales desc, num_curso desc, nivel_profesional desc;
"""

if platform.system()=="Windows":
    gf.ejecutar_comando ( "ciclo.py", "daw.yaml", "DAW")
    gf.ejecutar_comando ( "ciclo.py", "dawe.yaml", "DAWE")
    gf.ejecutar_comando ( "ciclo.py", "dam.yaml", "DAM")
    gf.ejecutar_comando ( "ciclo.py", "smir.yaml", "SMIR")
    gf.ejecutar_comando ( "ciclo.py", "smire.yaml", "SMIRE")
    gf.ejecutar_comando ( "ciclo.py", "fpb.yaml", "FPB")
    gf.ejecutar_comando ( "ciclo.py", "asir.yaml", "ASIR")
    gf.ejecutar_comando ( "ciclo.py", "mcom.yaml", "MCOM")
    gf.ejecutar_comando ( "ciclo.py", "sci.yaml", "SCI")
else:
    gf.ejecutar_comando ( "./ciclo.py", "daw.yaml", "DAW")
    gf.ejecutar_comando ( "./ciclo.py", "dawe.yaml", "DAWE")
    gf.ejecutar_comando ( "./ciclo.py", "dam.yaml", "DAM")
    gf.ejecutar_comando ( "./ciclo.py", "smir.yaml", "SMIR")
    gf.ejecutar_comando ( "./ciclo.py", "smire.yaml", "SMIRE")
    gf.ejecutar_comando ( "./ciclo.py", "fpb.yaml", "FPB")
    gf.ejecutar_comando ( "./ciclo.py", "asir.yaml", "ASIR")
    gf.ejecutar_comando ( "ciclo.py", "mcom.yaml", "MCOM")
    gf.ejecutar_comando ( "ciclo.py", "sci.yaml", "SCI")
    gf.ejecutar_comando(" echo ", "\".dump\"", "| sqlite3 ciclos.db ", "> bd.sql")
    gf.ejecutar_comando(" echo ", "\".mode csv \n.headers on"+EXTRACCION_MODULOS+"\"", "| sqlite3 ciclos.db ", "> modulos.csv")