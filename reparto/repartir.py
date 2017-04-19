#!/usr/bin/env python3
#coding=utf-8
from tkinter import *
from tkinter.messagebox import *
from Configurador import Configurador
from DialogoSimple import DialogoSimple

configurador=Configurador("..")
configurador.activar_configuracion("ciclos.settings")

from gestionbd.models import *
from reparto.models import *
from reparto.GeneradorInformesReparto import GeneradorInformesReparto

from random import randint

from django.db import transaction
from django.db.models import Q

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
        #self.etiqueta_horas["text"]=self.texto_horas.format(self.horas_asignadas)
        self.boton_profesor["text"]=self.modelo_profesor.nombre + "  ("+self.texto_horas.format(self.horas_asignadas)+")"
        
    def get_nombre_profesor(self):
        return self.modelo_profesor.nombre
    
    def crear_panel_profesor(self):    
        self.frame_profesor=Frame(self.frame_padre)
        
        self.boton_profesor=Button(self.frame_profesor, text=self.modelo_profesor.nombre)
        self.boton_profesor.padre=self.frame_profesor
        self.boton_profesor.profesor=self.modelo_profesor
        self.boton_profesor.pack(side=TOP, expand=True, fill=X)
        #self.etiqueta_horas=Label(self.frame_profesor)
        #self.etiqueta_horas.pack(side=TOP, expand=True, fill=X)
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
    
    def limpiar_modulos(self):
        for boton in self.botones_modulos:
            modulo=boton.modulo
            self.eliminar_modulo(modulo)
            
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
                self.botones_modulos.remove(boton)
                boton.destroy()

            #End del if
        #End del for
        return nuevo_boton_modulo
    
    def guardar_asignacion(self, objeto_reparto):
        
        for b in self.botones_modulos:
            objeto_modulo=b.modulo
            objeto_asignacion=Asignacion(
                reparto=objeto_reparto,
                profesor=self.modelo_profesor,
                modulo=objeto_modulo)
            objeto_asignacion.save()
        
    
    

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
        self.botones_modulos    =   []
        
        self.panel_modulo       =   self.crear_controles(padre)
        self.panel_profesores   =   self.crear_panel_profesores(padre)
        self.panel_modulo       =   self.crear_panel_modulos(padre)
        
        
        self.boton_profesor         =   None
        self.color_botones          =   None
        self.color_botones_destacado=   None
        
        self.anadir_modulos()
        self.anadir_profesores()
        
        
    def crear_controles(self, padre):
        #Creamos los menus
        self.barra_menus=Menu(padre)
        padre.config(menu=self.barra_menus)
        self.menu_archivo=Menu(self.barra_menus, tearoff=0)
        self.barra_menus.add_cascade(label="Archivo", menu=self.menu_archivo)
        self.menu_archivo.add_command(label="Abrir", command=self.abrir_reparto)
        
        
        self.frame_controles=Frame(padre)
        self.frame_controles.grid_rowconfigure(0, weight=1)
        self.frame_controles.grid_columnconfigure(0, weight=1)
        self.frame_controles.grid(row=0, column=0,  sticky=E+W)
        self.etiqueta_reparto=Label(self.frame_controles, text="Nombre del reparto")
        self.etiqueta_reparto.grid(row=0, column=0, sticky=E+W)
        
        self.txt_reparto=Entry(self.frame_controles)
        
        self.txt_reparto.delete(0, END)
        self.txt_reparto.insert(0, "Reparto_1")
        self.txt_reparto.grid(row=0, column=1, sticky=E+W)
        self.boton_guardar=Button(self.frame_controles, text="Guardar reparto")
        self.boton_guardar.grid(row=0, column=2, sticky=E+W)
        self.boton_guardar.bind("<ButtonRelease-1>", self.guardar_reparto)
        
        self.boton_limpiar_todo=Button(self.frame_controles, text="Limpiar reparto")
        self.boton_limpiar_todo.grid(row=0, column=3, sticky=W+E)
        self.boton_limpiar_todo.bind("<ButtonRelease-1>", self.limpiar_reparto)
        
    def limpiar_reparto(self, evento=None):
        for vista in self.vistas_profesores:
            vista.limpiar_modulos()
            
    def encontrar_vista(self, nombre_profesor):
        for v in self.vistas_profesores:
            if v.get_nombre_profesor()==nombre_profesor:
                return v
        return None
    
    def encontrar_boton(self, nombre_modulo):
        for boton_modulo in self.botones_modulos:
            if boton_modulo.modulo.nombre==nombre_modulo:
                return boton_modulo
        return None
    
    def abrir_reparto(self):
        dialogo_seleccion=DialogoSeleccion(self.frame_controles)
        if dialogo_seleccion.resultado!=None:
            #Cargamos el reparto
            
            reparto_elegido=Reparto.objects.get(nombre=dialogo_seleccion.resultado)
            self.txt_reparto.delete(0, END)
            self.txt_reparto.insert(0, reparto_elegido.nombre)
                
            asignaciones=Asignacion.objects.filter(reparto=reparto_elegido)
            self.limpiar_reparto()
            for a in asignaciones:
                modelo_profesor=a.profesor
                modelo_modulo=a.modulo
                vista_profesor=self.encontrar_vista(modelo_profesor.nombre)
                boton_modulo=self.encontrar_boton(modelo_modulo.nombre)
                self.asignar_modulo_a_profesor(vista_profesor, boton_modulo)
                print("Escribiendo:"+reparto_elegido.nombre)
                
                
            
    def guardar_reparto(self, evento):
        nombre_reparto=self.txt_reparto.get()
        if nombre_reparto=="":
            showerror("Nombre de reparto", "Primero se debe introducir un nombre de reparto")
            return
        #Comprobamos si ya se ha guardado información de este reparto
        reparto=Reparto.objects.all()
        if len(reparto)>0:
            confirmar_borrado=askyesno("Ya hay informacion",
                    "Ya hay información guardada para ese reparto\n¿desea sobreescribirla?")
            if confirmar_borrado==False:
                return
            else:
                reparto_para_borrar=Reparto.objects.filter(nombre=nombre_reparto)
                
                
                with transaction.atomic():
                    asignaciones_para_borrar=Asignacion.objects.filter(reparto=reparto_para_borrar)
                    for a in asignaciones_para_borrar:
                        a.delete()
                    reparto_para_borrar.delete()
                    
            
        #Si llegamos aquí se guardan todos los datos
        #almacenados en una única transacción
        with transaction.atomic():
            objeto_reparto=Reparto(nombre=nombre_reparto)
            objeto_reparto.save()
            for vista_profesor in self.vistas_profesores:
                vista_profesor.guardar_asignacion(objeto_reparto)
        #Una vez completada la transaccion guardamos los informes
        GeneradorInformesReparto.generar_informes()
        
    def crear_panel_profesores(self, padre):
        self.frame_profesores=Frame(padre)
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
        if len(texto) < 16:
            return texto
        linea_1=texto[0:16]
        linea_2=texto[17:31]
        linea=linea_1 + "\n"+linea_2+"..."
        return linea
        #return texto[0:longitud]+"..."
    
    def anadir_modulos(self):
        filtro_modulos_ps=Q(especialidad="PS")
        filtro_modulos_todos=Q(especialidad="TODOS")
        filtro_todos=filtro_modulos_ps  | filtro_modulos_todos 
        modulos=Modulo.objects.filter(filtro_todos).order_by("-horas_semanales")
        #modulos=Modulo.objects.filter(especialidad="PS").order_by("-horas_semanales")
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
        self.botones_modulos.append(boton)
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
        
        boton_modulo=evento.widget
        self.asignar_modulo_a_profesor(self.boton_profesor.vista_padre, boton_modulo)
        
    def asignar_modulo_a_profesor(self, vista_profesor, boton_modulo):
        fila_para_devolver_luego    =   boton_modulo.fila
        columna_para_devolver_luego =   boton_modulo.columna
        
        nuevo_boton_modulo=vista_profesor.asignar_modulo(boton_modulo.modulo, self.frame_modulos,
                            fila_para_devolver_luego, columna_para_devolver_luego)
        nuevo_boton_modulo.vista_padre=vista_profesor
        nuevo_boton_modulo.bind("<Button-1>", self.devolver_modulo)
        boton_modulo.destroy()
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
        
        
class DialogoSeleccion(DialogoSimple):
    def body(self, master):
        self.resultado=None
        self.listbox=Listbox(master)
        repartos=Reparto.objects.all().order_by("nombre")
        self.vector_elementos=dict()
        pos=0
        for r in repartos:
            self.listbox.insert(END,  r.nombre)
            self.vector_elementos[pos]=r.nombre
            pos+=1
        self.listbox.pack(side=TOP, expand=True, fill=BOTH)
        
        return self.listbox # initial focus

    def apply(self):
        posicion=self.listbox.curselection()
        posicion=posicion[0]
        
        self.resultado=self.vector_elementos[posicion]
        
if __name__ == '__main__':
    raiz=Tk()
    raiz.title("Reparto")
    repartidor=RepartirApp(raiz)
    raiz.grid_rowconfigure(0, weight=1)
    raiz.grid_rowconfigure(1, weight=4)
    raiz.grid_columnconfigure(0, weight=1)
    raiz.grid_columnconfigure(1, weight=3)
    raiz.mainloop()