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
        self.FILAS_MODULOS      =   10
        self.COLUMNAS_MODULOS   =   3
        
        self.panel_profesores   =   self.crear_panel_profesores(padre)
        self.panel_modulo       =   self.crear_panel_modulos(padre)
        self.profesor_seleccionado  =   None
        
        self.anadir_modulos()
        self.anadir_profesores()
        
    def crear_panel_profesores(self, padre):
        self.frame_profesores=Frame(padre, bg="blue")
        self.frame_profesores.grid_rowconfigure(0, weight=1)
        self.frame_profesores.grid_columnconfigure(0, weight=1)
        self.frame_profesores.grid(row=0, column=0, sticky=N+S+E+W)
        
    def crear_panel_modulos(self, padre):
        
        self.frame_modulos=Frame(padre, bg="red")
        for fila in range(0, self.FILAS_MODULOS+1):
            self.frame_modulos.grid_rowconfigure(fila, weight=1)
        for columna in range(0, self.COLUMNAS_MODULOS+1):
            self.frame_modulos.grid_columnconfigure(fila, weight=1)
        self.frame_modulos.grid(row=0, column=1, sticky=N+S+E+W)
        
        
    def anadir_modulos(self):
        modulos=Modulo.objects.filter(especialidad="PS").order_by("-horas_semanales")
        for modulo in modulos:
            self.anadir_modulo(modulo)
        
    def anadir_modulo(self, modulo):
        texto="{0}\n({1} horas-{2}{3})".format(
            modulo.nombre, modulo.horas_semanales,
            modulo.curso.ciclo.abreviatura, modulo.curso.num_curso)
        boton=Button(self.frame_modulos, text=texto)
        boton.grid(row=self.fila_actual, column=self.columna_actual, sticky=E+W+N+S)
        boton.modulo=modulo
        boton.bind("<Button-1>", self.click_modulo)
        boton.fila=self.fila_actual
        boton.columna=self.columna_actual
        self.columna_actual+=1
        if self.columna_actual==self.COLUMNAS_MODULOS:
            self.fila_actual+=1
            self.columna_actual=0
    
    def anadir_profesores(self):
        esp_ps=EspecialidadProfesor.objects.filter(especialidad="PS")
        profesores=Profesor.objects.filter(especialidad=esp_ps).order_by("num_posicion")
        fila_profesor=0
        for profesor in profesores:
            self.frame_profesores.grid_rowconfigure(fila_profesor, weight=1)
            fila_profesor+=1
            
        fila_profesor=0
        for profesor in profesores:
            print(profesor, profesor.num_posicion)
            boton=Button(self.frame_profesores, text=profesor.nombre)
            boton.profesor=profesor
            boton.grid(row=fila_profesor, sticky=E+W+N+S)
            fila_profesor+=1
            boton.bind("<Button-1>", self.click_profesor)
            
    def click_profesor(self, evento):
        profesor=evento.widget.profesor
        print ("Click en profesor:"+profesor.nombre)
        self.profesor_seleccionado=profesor
        
    def click_modulo(self, evento):
        modulo=evento.widget.modulo
        self.profesor_seleccionado  =   None
if __name__ == '__main__':
    raiz=Tk()
    repartidor=RepartirApp(raiz)
    raiz.grid_rowconfigure(0, weight=1)
    raiz.grid_columnconfigure(0, weight=1)
    raiz.grid_columnconfigure(1, weight=4)
    raiz.mainloop()