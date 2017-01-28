#!/usr/bin/env python3


from tkinter import *
from tkinter.ttk import *
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
        #Se necesita tenerlo creado al empezar
        self.frame_cursos=None
        self.frame_modulos=None
    
    def _crear_cuadro_inferior(self):
        cuaderno=Notebook(self.ventana)
        tabs=["Obj generales", "Obj especificos"]
        for t in tabs:
            frame_tab=Frame(cuaderno)
            frame_tab.pack()
            cuaderno.add(frame_tab, text=t)
            
        cuaderno.pack(side=BOTTOM)
            
        
    
    def crear_frame_ciclos(self):
        self.frame_ciclos=Frame(self.ventana)
        self.frame_ciclos.pack(side=LEFT, fill=Y)
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
    
    
    def destruir_botones(self, _frame):
        if _frame==None:
            return 
        for control in _frame.slaves():
            control.destroy()
            
    ####Gestión de eventos######
    
    def _on_ciclo_elegido(self, evento):
        texto_boton_pulsado=evento.widget.nombre
        ciclo_elegido=self.todos_ciclos.filter(nombre=texto_boton_pulsado)
        #print(ciclo_elegido)
        if self.frame_cursos==None:
            self.frame_cursos=Frame(self.ventana)
            self.frame_cursos.pack(side=LEFT, fill=Y)
        else:
            self.destruir_botones(self.frame_cursos)
            self.destruir_botones(self.frame_modulos)
            
        self._mostrar_cursos_asociados_a_ciclo(ciclo_elegido)
            
    def _mostrar_cursos_asociados_a_ciclo(self, modelo_ciclo):
        cursos_asociados=self.todos_cursos.filter(ciclo=modelo_ciclo)
        #print(cursos_asociados)
        for c in cursos_asociados:
            btn_curso=Button(self.frame_cursos, text=c.nombre_curso)
            btn_curso.pack(fill=X)
            btn_curso.nombre=c.nombre_curso
            btn_curso.bind("<Button-1>", self._on_curso_elegido)
        return self.frame_cursos
        
    def _on_curso_elegido(self, evento):
        texto_boton_pulsado=evento.widget.nombre
        curso_elegido=self.todos_cursos.filter(nombre_curso=texto_boton_pulsado)
        if self.frame_modulos==None:
            self.frame_modulos=Frame(self.ventana)
            self.frame_modulos.pack(side=LEFT, fill=Y)
        else:
            self.destruir_botones(self.frame_modulos)
            
        self._mostrar_modulos_asociados_a_curso(curso_elegido)
    
    def _mostrar_modulos_asociados_a_curso(self, modelo_curso):
        modulos_asociados=self.todos_modulos.filter(curso=modelo_curso)
        #print(cursos_asociados)
        for m in modulos_asociados:
            btn_modulo=Button(self.frame_modulos, text=m.nombre)
            btn_modulo.pack(fill=X)
            btn_modulo.nombre=m.nombre
            btn_modulo.bind("<Button-1>", self._on_modulo_elegido)
        return self.frame_modulos
        
    def _on_modulo_elegido(self, evento):
        texto_boton_pulsado=evento.widget.nombre
        #Ojo, al filtrar puede haber muchos con el mismo nombre, por eso
        #nos quedamos solo con el primero
        modulo_elegido=self.todos_modulos.filter(nombre=texto_boton_pulsado)[0]
        print(modulo_elegido)

if __name__ == '__main__':
    app=Interfaz()
    
    
    

