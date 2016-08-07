#!/usr/bin/env python3
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("ciclos")
configurador.activar_configuracion ("ciclos.settings")
from gestionbd.models import Modulo, Profesor
from django.db.models.expressions import Q
import sys

paquete=sys.argv[1]

        

filtrado=~Q(especialidad="PT")
modulos=Modulo.objects.filter(filtrado)
print ("package {0};".format(paquete))
print ("public class Inicializador")
print ("\tpublic static Modulo[] getModulos(){")
print("\t\tModulo[] modulos=new Modulo[{0}];".format(len(modulos)))
i=0
for m in modulos:
    print("\t\t"+m.to_java("modulos", i)+";")
    i=i+1
print ("\t}")
print ("}")
