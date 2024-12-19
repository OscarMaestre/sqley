#!/usr/bin/env python3
#coding=utf-8


import os
import sys
import django

class Configurador(object):
    def __init__(self, ruta_proyecto):
        """
            Configura django para que podamos importar los modelos
            
            
                Argumentos:
                
                    ruta_proyecto -- Ruta al proyecto que contiene los settings
        """
        sys.path.append ( ruta_proyecto )
        
    def activar_configuracion(self, paquete_settings):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', paquete_settings)
        django.setup()