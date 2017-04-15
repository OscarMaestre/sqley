#!/usr/bin/env python3
#coding=utf-8
from tkinter import *
from utilidades.basedatos.Configurador import Configurador

configurador=Configurador("..")
configurador.activar_configuracion("ciclos.settings")

from gestionbd.models import *
from random import randint


class VistaProfesor(object):
    def __init__(self, profesor, frame_padre):
        self.boton_profesor=None
        self.botones_modulos=[]
        self.horas_asignadas=0
        self.horas_minimas=profesor.horas_minimas
        self.texto_horas="{0}/"+str(self.horas_minimas)
        
        self.frame_padre=frame_padre
        self.modelo_profesor=profesor
        
        
    def cambiar_etiqueta(self):
        self.etiqueta_horas["text"]=self.texto_horas.format(self.horas_asignadas)
    def crear_panel_profesor(self):    
        self.frame_profesor=Frame(self.frame_padre)
        
        self.boton_profesor=Button(self.frame_profesor, text=self.modelo_profesor.nombre)
        self.boton_profesor.padre=self.frame_profesor
        self.boton_profesor.profesor=self.modelo_profesor
        self.boton_profesor.pack(side=TOP, expand=True, fill=X)
        self.etiqueta_horas=Label(self.frame_profesor)
        self.etiqueta_horas.pack(side=TOP, expand=True, fill=X)
        self.cambiar_etiqueta()
        return self.frame_profesor
    
    def get_boton_profesor(self):
        return self.boton_profesor
    
    def recortar_nombre(self, texto, longitud=32):
        return texto[0:longitud]+"..."
    
    def asignar_modulo(self, modelo_modulo, padre_anterior, fila, columna):
        texto_modulo="{0}\n({1} horas-{2}{3})".format(
                    self.recortar_nombre(modelo_modulo.nombre),
                    modelo_modulo.horas_semanales,
                    modelo_modulo.curso.ciclo.abreviatura,
                    modelo_modulo.curso.num_curso)
        boton_modulo=Button(self.frame_profesor, text=texto_modulo)
        boton_modulo.modulo=modelo_modulo
        boton_modulo.fila=fila
        boton_modulo.columna=columna
        boton_modulo.padre_anterior=padre_anterior
        boton_modulo.pack(side=LEFT)
        self.botones_modulos.append(boton_modulo)
        self.horas_asignadas+=modelo_modulo.horas_semanales
        self.cambiar_etiqueta()
        return boton_modulo
    
    def eliminar_modulo(self, modelo_modulo):
        nuevo_boton_modulo=None
        for boton in self.botones_modulos:
            modulo=boton.modulo
            if modulo==modelo_modulo:
                self.horas_asignadas-=modelo_modulo.horas_semanales
                padre_anterior=boton.padre_anterior
                
                texto="{0}\n({1} horas-{2}{3})".format(
                    self.recortar_nombre(modulo.nombre),  modulo.horas_semanales,
                    modulo.curso.ciclo.abreviatura, modulo.curso.num_curso)
                nuevo_boton_modulo=Button(padre_anterior, text=texto)
                nuevo_boton_modulo.grid(row=boton.fila, column=boton.columna, sticky=E+W+N+S)
                self.cambiar_etiqueta()
                boton.destroy()

            #End del if
        #End del for
        return nuevo_boton_modulo
    
    def guardar_asignacion(self):
        print("Guardando para "+str(self.modelo_profesor.nombre))
        for b in self.botones_modulos:
            modulo=b.modulo
            print("\t"+modulo.nombre)
    
    

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
        self.COLUMNAS_MODULOS   =   5
        
        self.NUM_FILA_MODULOS   =   1
        self.NUM_COL_MODULOS    =   1
        self.NUM_FILA_PROFESORES=   1
        self.NUM_COL_PROFESORES =   0
        
        
        self.vistas_profesores  =   []
        
        self.panel_profesores   =   self.crear_panel_profesores(padre)
        self.panel_modulo       =   self.crear_panel_modulos(padre)
        self.panel_modulo       =   self.crear_controles(padre)
        
        self.boton_profesor         =   None
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
        self.boton_guardar=Button(self.frame_controles, text="Guardar reparto")
        self.boton_guardar.grid(row=0, column=2, sticky=N+S+E+"")
        self.boton_guardar.bind("<Button-1>", self.guardar_reparto)
        
    def guardar_reparto(self, evento):
        for vista_profesor in self.vistas_profesores:
            vista_profesor.guardar_asignacion()
        
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
        
        
        
    def crear_boton_modulo(self, padre, modulo):
        texto="{0}\n({1} horas-{2}{3})".format(
            self.recortar_nombre(modulo.nombre),  modulo.horas_semanales,
            modulo.curso.ciclo.abreviatura, modulo.curso.num_curso)
        boton=Button(padre, text=texto)
        boton.modulo=modulo
        return boton
    
    def anadir_modulo(self, modulo):
        boton=self.crear_boton_modulo(self.frame_modulos, modulo)
        
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
            vista_profesor=VistaProfesor(profesor, self.frame_profesores)
            self.vistas_profesores.append(vista_profesor)
            panel_profesor=vista_profesor.crear_panel_profesor()
            boton_profesor=vista_profesor.get_boton_profesor()
            boton_profesor.vista_padre=vista_profesor
            boton_profesor.bind("<Button-1>", self.click_profesor)
            #panel_profesor=self.crear_panel_profesor(self.frame_profesores, profesor)
            #print(profesor, profesor.num_posicion)
            panel_profesor.grid(row=fila_profesor, sticky=E+W+N+S)
            fila_profesor+=1
            continue
            
        
    def click_profesor(self, evento):
        if self.boton_profesor!=None:
            self.desactivar_destacado(self.boton_profesor)
        self.boton_profesor=evento.widget
        self.activar_destacado(self.boton_profesor)
        
    def activar_destacado(self, widget):
        self.colorear_control(widget)
        
        
    def desactivar_destacado(self, widget):
        self.colorear_control(widget, self.color_botones, self.color_botones_destacado)
        
        
    def colorear_control(self, widget, color="red", color_destacado="#dd0000"):
        widget["bg"]=color
        widget["highlightcolor"]=color
        
        
    def click_modulo(self, evento):
        if self.boton_profesor==None:
            return 
        
        modulo=evento.widget.modulo
        
        fila_para_devolver_luego    =   evento.widget.fila
        columna_para_devolver_luego =   evento.widget.columna
        
        vista_profesor=self.boton_profesor.vista_padre
        nuevo_boton_modulo=vista_profesor.asignar_modulo(modulo, self.frame_modulos,
                            fila_para_devolver_luego, columna_para_devolver_luego)
        nuevo_boton_modulo.vista_padre=vista_profesor
        nuevo_boton_modulo.bind("<Button-1>", self.devolver_modulo)
        evento.widget.destroy()
        return 
        
        
    def devolver_modulo(self, evento):
        boton_modulo_pulsado=evento.widget
        vista_profesor_padre=boton_modulo_pulsado.vista_padre
        vista_profesor_padre.eliminar_modulo(boton_modulo_pulsado.modulo)
        fila_a_la_que_devolver=boton_modulo_pulsado.fila
        columna_a_la_que_devolver=boton_modulo_pulsado.columna
        boton_modulo=self.crear_boton_modulo(self.frame_modulos, evento.widget.modulo)
        boton_modulo.grid(row=fila_a_la_que_devolver,
                          column=columna_a_la_que_devolver,
                          sticky=E+W+N+S)
        
        boton_modulo.bind("<Button-1>", self.click_modulo)
        boton_modulo.fila=self.fila_actual
        boton_modulo.columna=self.columna_actual
        evento.widget.destroy()
        
        
if __name__ == '__main__':
    raiz=Tk()
    raiz.title("Reparto")
    repartidor=RepartirApp(raiz)
    raiz.grid_rowconfigure(0, weight=1)
    raiz.grid_rowconfigure(1, weight=4)
    raiz.grid_columnconfigure(0, weight=1)
    raiz.grid_columnconfigure(1, weight=3)
    raiz.mainloop()