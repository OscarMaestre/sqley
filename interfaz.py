#!/usr/bin/env python3


from tkinter import *

import os   
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("ciclos")
configurador.activar_configuracion ("ciclos.settings")

from gestionbd.models import *


class Interfaz(object):
    def __init__(self):
        self.todos_objetivos_generales  =   ObjetivoGeneral.objects.all()
        self.todos_ciclos               =   Ciclo.objects.all()
        self.todos_cursos               =   Curso.objects.all()
        self.todos_modulos              =   Modulo.objects.all()
        
        self._crear_gui()
        
        return
    
    def _crear_gui(self):
        self.ventana=Tk()
        self._crear_cuadro_superior()
        self._crear_cuadro_inferior()
        self.ventana.mainloop()
        
        
    def _crear_cuadro_superior(self):
        self.crear_frame_ciclos()
        pass
    
    def _crear_cuadro_inferior(self):
        pass
    
    def crear_frame_ciclos(self):
        self.frame_ciclos=Frame(self.ventana)
        self.frame_ciclos.pack()
        for c in self.todos_ciclos:
            btn_ciclo=Button(self.frame_ciclos, text=c.nombre)
            btn_ciclo.pack(fill=X)
            btn_ciclo.nombre=c.nombre
            btn_ciclo.bind("<Button-1>", self._on_ciclo_elegido)
        return self.frame_ciclos
    
    def get_cadenas(modelos, tupla_configuracion):
        lista_textos=[]
        for m in modelos:
            lista_textos.append(m.__dict__[tupla_configuracion[1]])
        return lista_textos
    
    ####Gestión de eventos######
    
    def _on_ciclo_elegido(self, evento):
        texto_boton_pulsado=evento.widget.nombre
        ciclo_elegido=self.todos_ciclos.filter(nombre=texto_boton_pulsado)
        print(ciclo_elegido)
        
        
        

if __name__ == '__main__':
    app=Interfaz()
    
    
    

