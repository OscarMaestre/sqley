#!/usr/bin/env python3


import os   
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("ciclos")
configurador.activar_configuracion ("ciclos.settings")

from gestionbd.models import *

from kivy.app import App
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.tabbedpanel import TabbedPanelHeader
datos=[]



tuplas_tablas=[
    (Ciclo,"nombre"), (Curso, "nombre_curso"), (Modulo, "nombre")
]

def conversor(indice, cadena):
    diccionario={
        "text":cadena,
        "is_selected":False,
        'height':25
    }
    return diccionario

def get_adaptador(modelos, tupla_configuracion):
    lista_textos=get_cadenas(modelos, tupla_configuracion)
    adaptador=ListAdapter(data=lista_textos, args_converter=conversor,
                          cls=ListItemButton, selection_mode='single',
                          allow_empty_selection=False)
    return adaptador

def get_cadenas(modelos, tupla_configuracion):
    lista_textos=[]
    for m in modelos:
        lista_textos.append(m.__dict__[tupla_configuracion[1]])
    return lista_textos

    
    
class FabricaTabs(object):
    @staticmethod
    def get_tab_objetivos(texto_tab):
        tab=TabbedPanelHeader(text=texto_tab)
        tab.content=Button(text=texto_tab)
        return tab
    
class GuiApp(App):
    def algo_seleccionado(self, adaptador):
        print("Ok")
        print (adaptador.selection)
        
    
    
    def on_ciclo_seleccionado(self, boton):
        ciclo_seleccionado=self.todos_ciclos.get(nombre=boton.text)
        print(ciclo_seleccionado)
        self.crear_botones_cursos(ciclo_seleccionado)
        
    def on_curso_seleccionado(self, boton):
        contenedor_cursos=self.root.ids.contenedor_cursos
        print (boton.text)
        curso_seleccionado=self.todos_cursos.get(nombre_curso=boton.text)
        print(curso_seleccionado)
        self.crear_botones_modulos(curso_seleccionado)
        
    def on_modulo_seleccionado(self, boton):
        print (boton.text)
        
    def crear_botones_ciclos(self):
        contenedor_ciclos=self.root.ids.contenedor_ciclos
        lista_ciclos=get_cadenas(self.todos_ciclos, tuplas_tablas[0])
        for ciclo in lista_ciclos:
            #btn_ciclo=Button(text=ciclo, height=45)
            btn_ciclo=ToggleButton(text=ciclo, height=45, group="ciclos")
            btn_ciclo.bind(on_press=self.on_ciclo_seleccionado)
            contenedor_ciclos.add_widget(btn_ciclo)
            
    def crear_botones_cursos(self, ciclo_seleccionado):
        contenedor_cursos=self.root.ids.contenedor_cursos
        contenedor_cursos.clear_widgets()
        lista_cursos_asociados=self.todos_cursos.filter(ciclo_id=ciclo_seleccionado.id)
        for curso in lista_cursos_asociados:
            btn_curso=ToggleButton(text=curso.nombre_curso, height=45, group="cursos")
            btn_curso.bind(on_press=self.on_curso_seleccionado)
            contenedor_cursos.add_widget(btn_curso)
            
    def crear_botones_modulos(self, curso_seleccionado):
        contenedor_modulos=self.root.ids.contenedor_modulos
        contenedor_modulos.clear_widgets()
        lista_modulos=self.todos_modulos.filter(curso_id=curso_seleccionado.id)
        for m in lista_modulos:
            btn_modulo=ToggleButton(text=m.nombre, height=45, group="modulos")
            btn_modulo.bind(on_press=self.on_modulo_seleccionado)
            contenedor_modulos.add_widget(btn_modulo)
    
    def crear_tabs(self):
        contenedor_tabs=self.root.ids.tabs
        contenedor_tabs.add_widget(FabricaTabs.get_tab_objetivos("Objetivos generales"))
        
        
    def on_start(self):
        self.todos_ciclos=Ciclo.objects.all()
        self.todos_cursos=Curso.objects.all()
        self.todos_modulos=Modulo.objects.all()
        self.crear_botones_ciclos()
        #Al principio necesitamos borrar todos los tabs
        contenedor_modulos=self.root.ids.tabs.clear_tabs()
        self.crear_tabs()
        return 
        
        
        

if __name__ == '__main__':
    GuiApp().run()
    
    
    