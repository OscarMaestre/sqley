#!/usr/bin/env python3
from utilidades.ficheros.GestorFicheros import GestorFicheros
import sys

f=open(sys.argv[1], encoding="utf-8")
lineas=f.readlines()
for l in lineas:
    print (l)

