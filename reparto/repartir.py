#!/usr/bin/env python3

from tkinter import *
from utilidades.basedatos.Configurador import Configurador

configurador=Configurador("..")
configurador.activar_configuracion("ciclos.settings")

from gestionbd.models import *

class RepartirApp(object):
    
    def __init__(self, padre):
        self.fila_actual        =   0
        self.columna_actual     =   0
        self.FILAS_MODULOS      =   7
        self.COLUMNAS_MODULOS   =   4
        
        self.panel_profesores   =   self.crear_panel_profesores(padre)
        self.panel_modulo       =   self.crear_panel_modulos(padre)
        self.anadir_modulos()
    def crear_panel_profesores(self, padre):
        self.frame_profesores=Frame(padre)
        self.frame_profesores.grid_rowconfigure(0, weight=1)
        self.frame_profesores.grid_columnconfigure(0, weight=1)
        self.frame_profesores.grid(row=0, column=0)
        
    def crear_panel_modulos(self, padre):
        
        self.frame_modulos=Frame(padre)
        for fila in range(0, self.FILAS_MODULOS+1):
            self.frame_modulos.grid_rowconfigure(fila, weight=1)
        for columna in range(0, self.COLUMNAS_MODULOS+1):
            self.frame_modulos.grid_columnconfigure(fila, weight=1)
        self.frame_modulos.grid(row=0, column=0)
        
    def anadir_modulos(self):
        modulos=Modulo.objects.all()
        for modulo in modulos:
            self.anadir_modulo(modulo.nombre, modulo.horas_semanales, modulo.curso)
        
    def anadir_modulo(self, nombre, horas, curso):
        texto="{0} ({1} horas)".format(nombre, horas)
        boton=Button(self.frame_modulos, text=texto)
        boton.grid(row=self.fila_actual, column=self.columna_actual, sticky=E+W)
        self.columna_actual+=1
        if self.columna_actual==self.COLUMNAS_MODULOS:
            self.fila_actual+=1
            self.columna_actual=0
    
if __name__ == '__main__':
    raiz=Tk()
    repartidor=RepartirApp(raiz)
    raiz.mainloop()