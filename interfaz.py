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
        self.todas_competencias_generales=  CompetenciaGeneral.objects.all()
        self.todas_competencias         =   Competencia.objects.all()
        self.todas_cualificaciones      =   CualificacionProfesional.objects.all()
        
        self.todos_ciclos               =   Ciclo.objects.all()
        self.todos_cursos               =   Curso.objects.all()
        self.todos_modulos              =   Modulo.objects.all()
        
        self._crear_gui()
        
        return
    
    def _crear_gui(self):
        self.crear_valores_iniciales()
        self.ventana=Tk()
        
        self.cuadro_superior=Frame(self.ventana)
        self.cuadro_superior.pack()
        self.cuadro_inferior=Frame(self.ventana)
        self.cuadro_inferior.pack(fill=BOTH, expand=True)
        
        self._crear_cuadro_superior(self.cuadro_superior)
        self._crear_cuadro_inferior(self.cuadro_inferior)
        self.ventana.mainloop()
        
        
        
    def _crear_cuadro_superior(self, frame_padre):
        self.crear_frame_ciclos(frame_padre)
        #Se necesita tenerlo creado al empezar
        self.frame_cursos=None
        self.frame_modulos=None
    
    def crear_valores_iniciales(self):
        self.nombres_tabs=["Obj generales del ciclo", "Competencias generales", "Competencias", "Cualificaciones"]
        self.OBJETIVOS_GENERALES        =0
        self.COMPETENCIAS_GENERALES     =1
        self.COMPETENCIAS               =2
        self.CUALIFICACION              =3
        
    def _crear_cuadro_inferior(self, frame_padre):
        cuaderno=Notebook(frame_padre)
        self.tabs=[]
        for t in self.nombres_tabs:
            frame_tab=Frame(cuaderno)
            self.tabs.append(frame_tab)
            frame_tab.pack()
            cuaderno.add(frame_tab, text=t)
            
        cuaderno.pack(side=BOTTOM)
            
        
    
    def crear_boton(self, frame_padre, texto, funcion):
        btn=Button(frame_padre, text=texto)
        btn.pack(fill=X, padx=10, pady=2)
        btn.nombre=texto
        btn.bind("<Button-1>", funcion)
        return btn
        
    def crear_frame_ciclos(self, frame_padre):
        self.frame_ciclos=Frame(frame_padre)
        self.frame_ciclos.pack(side=LEFT, fill=Y)
        for c in self.todos_ciclos:
            self.crear_boton(self.frame_ciclos, c.nombre, self._on_ciclo_elegido)
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
            self.frame_cursos=Frame(self.cuadro_superior)
            self.frame_cursos.pack(side=LEFT, fill=Y)
        else:
            self.destruir_botones(self.frame_cursos)
            self.destruir_botones(self.frame_modulos)
            
        self._mostrar_cursos_asociados_a_ciclo(ciclo_elegido)
        
        self.rellenar_notebook_segun_ciclo(ciclo_elegido)
        
    def rellenar_notebook_segun_ciclo(self, ciclo_elegido):
        self.rellenar_objetivos_generales       (   ciclo_elegido   )
        self.rellenar_competencias_generales    (   ciclo_elegido   )
        self.rellenar_competencias              (   ciclo_elegido   )
        self.rellenar_cualificaciones           (   ciclo_elegido   )
            
    def _mostrar_cursos_asociados_a_ciclo(self, modelo_ciclo):
        cursos_asociados=self.todos_cursos.filter(ciclo=modelo_ciclo)
        #print(cursos_asociados)
        for c in cursos_asociados:
            self.crear_boton(self.frame_cursos, c.nombre_curso, self._on_curso_elegido)
        return self.frame_cursos
        
    def _on_curso_elegido(self, evento):
        texto_boton_pulsado=evento.widget.nombre
        curso_elegido=self.todos_cursos.filter(nombre_curso=texto_boton_pulsado)
        if self.frame_modulos==None:
            self.frame_modulos=Frame(self.cuadro_superior)
            self.frame_modulos.pack(side=LEFT, fill=Y)
        else:
            self.destruir_botones(self.frame_modulos)
            
        self._mostrar_modulos_asociados_a_curso(curso_elegido)
    
    def _mostrar_modulos_asociados_a_curso(self, modelo_curso):
        modulos_asociados=self.todos_modulos.filter(curso=modelo_curso)
        #print(cursos_asociados)
        for m in modulos_asociados:
            self.crear_boton(self.frame_modulos, m.nombre, self._on_modulo_elegido)
        return self.frame_modulos
        
    def _on_modulo_elegido(self, evento):
        texto_boton_pulsado=evento.widget.nombre
        #Ojo, al filtrar puede haber muchos con el mismo nombre, por eso
        #nos quedamos solo con el primero
        modulo_elegido=self.todos_modulos.filter(nombre=texto_boton_pulsado)[0]
        #print(modulo_elegido)
        
    def rellenar_objetivos_generales(self, ciclo_elegido):
        
        objetivos_ciclos=self.todos_objetivos_generales.filter(ciclo=ciclo_elegido)
        cadenas=[]
        for o in objetivos_ciclos:
            cadenas.append(o.letra+") "+o.texto)
        
        self.destruir_botones(self.tabs[self.OBJETIVOS_GENERALES])
        self.crear_tabs(self.tabs[self.OBJETIVOS_GENERALES], "objetivos generales", cadenas)
        
    def rellenar_competencias_generales(self, ciclo_elegido):
        competencias_generales=self.todas_competencias_generales.filter(ciclo=ciclo_elegido)
        cadenas=[]
        for c in competencias_generales:
            cadenas.append(c.texto)
            
        self.destruir_botones(self.tabs[self.COMPETENCIAS_GENERALES])
        self.crear_tabs(self.tabs[self.COMPETENCIAS_GENERALES], "competencias generales", cadenas)
        
    def rellenar_competencias(self, ciclo_elegido):
        competencias=self.todas_competencias.filter(ciclo=ciclo_elegido)
        cadenas=[]
        for c in competencias:
            cadenas.append(c.texto)
            
        self.destruir_botones(self.tabs[self.COMPETENCIAS])
        self.crear_tabs(self.tabs[self.COMPETENCIAS], "competencias", cadenas)
        
    def rellenar_cualificaciones(self, ciclo_elegido):
        cualificaciones=self.todas_cualificaciones.filter(ciclo=ciclo_elegido)
        cadenas=[]
        for c in cualificaciones:
            cadenas.append(c.texto)
            
        self.destruir_botones(self.tabs[self.CUALIFICACION])
        self.crear_tabs(self.tabs[self.CUALIFICACION], "cualificaciones profesionales", cadenas)
        
    
    def crear_tabs(self, control_padre, letrero, lista_cadenas):
        frame_controles=Frame(control_padre)
        frame_controles.pack()
        
        btn_marcar_todo=Button(frame_controles, text="Marcar/desmarcar todo" )
        btn_marcar_todo.pack(fill=X)
        btn_marcar_todo.checkboxes=[]
        btn_marcar_todo.valor=True
        btn=Button(frame_controles, text="Copiar al portapapeles los elementos marcados" )
        btn.pack(fill=X)
        btn.checkboxes=[]
        btn.origen=letrero
        btn.bind("<Button-1>", self.extraer_los_checkboxes_marcados)
        btn_marcar_todo.bind("<Button-1>", self.conmutar_todo)
        frame_checkboxes=Frame(frame_controles)
        frame_checkboxes.pack(side=LEFT)
        
        for cad in lista_cadenas:
            var_asociada=BooleanVar()
            var_asociada.set(False)
            checkbox=Checkbutton(frame_checkboxes, text=cad, variable=var_asociada)
            checkbox.var_asociada=var_asociada
            checkbox.pack(fill=X)
            
            checkbox.texto=cad
            btn.checkboxes.append(checkbox)
            btn_marcar_todo.checkboxes.append(checkbox)
            
    def extraer_los_checkboxes_marcados(self, evento):
        textos=[]
        for control in evento.widget.checkboxes:
            if control.var_asociada.get()==True:
                textos.append(control.texto)
                #print (control.texto)
        self.ventana.clipboard_clear()
        self.ventana.clipboard_append("\n".join(textos))
        
    def conmutar_todo(self, evento):
        for control in evento.widget.checkboxes:
            control.var_asociada.set(evento.widget.valor)
        evento.widget.valor= not evento.widget.valor
            
    def desmarcar_todo(self, evento):
        for control in evento.widget.checkboxes:
            control.var_asociada.set(False)
        
if __name__ == '__main__':
    app=Interfaz()
    
    
    

