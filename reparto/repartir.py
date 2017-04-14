#!/usr/bin/env python3

from tkinter import *
from utilidades.basedatos.Configurador import Configurador

configurador=Configurador("..")
configurador.activar_configuracion("ciclos.settings")

from gestionbd.models import *
from random import randint


class ConstructorObjetos(object):
    @staticmethod
    def construir_frame(padre, filas, columnas, pesos_filas=None, pesos_columnas=None):
        panel=Frame(padre)
        if pesos_filas==None:
            pesos_filas=[1]*filas
        if pesos_columnas==None:
            pesos_columnas=[1]*columnas
        #print(pesos_columnas,pesos_filas)
        for fila in range(0, filas):
            #print(fila, pesos_filas[fila])
            panel.grid_rowconfigure(fila, weight=pesos_filas[fila])
        for columna in range(0, columnas):
            panel.grid_columnconfigure(columna, weight=pesos_columnas[columna])
        return panel
    
        
class RepartirApp(object):
    
    def __init__(self, padre):
        self.fila_actual        =   0
        self.columna_actual     =   0
        self.FILAS_MODULOS      =   10
        self.COLUMNAS_MODULOS   =   3
        
        self.NUM_FILA_MODULOS   =   1
        self.NUM_COL_MODULOS    =   1
        self.NUM_FILA_PROFESORES=   1
        self.NUM_COL_PROFESORES =   0
        
        self.panel_profesores   =   self.crear_panel_profesores(padre)
        self.panel_modulo       =   self.crear_panel_modulos(padre)
        self.panel_modulo       =   self.crear_controles(padre)
        self.profesor_seleccionado  =   None
        self.widget_profesor        =   None
        self.color_botones          =   None
        self.color_botones_destacado=   None
        self.anadir_modulos()
        self.anadir_profesores()
        
        
    def crear_controles(self, padre):
        self.frame_controles=Frame(padre, bg="blue")
        self.frame_controles.grid_rowconfigure(0, weight=1)
        self.frame_controles.grid_columnconfigure(0, weight=1)
        self.frame_controles.grid(row=0, column=0,  sticky=N+S+E+W)
        self.etiqueta_reparto=Label(self.frame_controles, text="Nombre del reparto")
        self.etiqueta_reparto.grid(row=0, column=0, sticky=N+S+E+W)
        
        self.txt_reparto=Entry(self.frame_controles, text="Hola")
        self.txt_reparto.grid(row=0, column=1, sticky=N+S+E+W)
        
    def crear_panel_profesores(self, padre):
        self.frame_profesores=Frame(padre, bg="green")
        self.frame_profesores.grid_rowconfigure(0, weight=1)
        self.frame_profesores.grid_columnconfigure(0, weight=1)
        self.frame_profesores.grid(row=self.NUM_FILA_PROFESORES,
                                   column=self.NUM_COL_PROFESORES, sticky=N+S+E+W)
        
    def crear_panel_modulos(self, padre):
        self.frame_modulos=ConstructorObjetos.construir_frame(padre,
                                        self.FILAS_MODULOS, self.COLUMNAS_MODULOS)
        self.frame_modulos.grid(row=self.NUM_FILA_MODULOS,
                                column=self.NUM_COL_MODULOS, sticky=N+S+E+W)
        return 
        
        
    def recortar_nombre(self, texto, longitud=32):
        return texto[0:longitud]+"..."
    
    def anadir_modulos(self):
        modulos=Modulo.objects.filter(especialidad="PS").order_by("-horas_semanales")
        for modulo in modulos:
            self.anadir_modulo(modulo)
        
    def anadir_modulo(self, modulo):
        texto="{0}\n({1} horas-{2}{3})".format(
            self.recortar_nombre(modulo.nombre),  modulo.horas_semanales,
            modulo.curso.ciclo.abreviatura, modulo.curso.num_curso)
        boton=Button(self.frame_modulos, text=texto)
        self.color_botones=boton["bg"]
        self.color_botones_destacado=boton["highlightcolor"]
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
            panel_profesor=self.crear_panel_profesor(self.frame_profesores, profesor)
            #print(profesor, profesor.num_posicion)
            panel_profesor.grid(row=fila_profesor, sticky=E+W+N+S)
            fila_profesor+=1
            continue
            
    def crear_panel_profesor(self, padre, profesor):
        
        frame_profesor=Frame(padre)
        
        boton=Button(frame_profesor, text=profesor.nombre)
        boton.profesor=profesor
        boton.padre=frame_profesor
        boton.bind("<Button-1>", self.click_profesor)
        boton.pack(side=TOP, expand=True, fill=X)
        return frame_profesor
        
    def click_profesor(self, evento):
        if self.widget_profesor!=None:
            self.desactivar_destacado(self.widget_profesor)
        profesor=evento.widget.profesor
        print ("Click en profesor:"+profesor.nombre)
        self.profesor_seleccionado=profesor
        self.widget_profesor=evento.widget
        self.activar_destacado(self.widget_profesor)
        
    def activar_destacado(self, widget):
        self.colorear_control(widget)
        
        
    def desactivar_destacado(self, widget):
        self.colorear_control(widget, self.color_botones, self.color_botones_destacado)
        
        
    def colorear_control(self, widget, color="red", color_destacado="#dd0000"):
        widget["bg"]=color
        widget["highlightcolor"]=color
        
        
    def click_modulo(self, evento):
        modulo=evento.widget.modulo
        frame_para_insertar_boton_modulo=self.widget_profesor.padre
        print(frame_para_insertar_boton_modulo)
        #Crear boton copia
        self.profesor_seleccionado  =   None
        self.widget_profesor["bg"]=self.color_botones
        self.widget_profesor=None
        
        
        
if __name__ == '__main__':
    raiz=Tk()
    repartidor=RepartirApp(raiz)
    raiz.grid_rowconfigure(0, weight=1)
    raiz.grid_rowconfigure(1, weight=4)
    raiz.grid_columnconfigure(0, weight=1)
    raiz.grid_columnconfigure(1, weight=3)
    raiz.mainloop()