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
from kivy.uix.boxlayout import BoxLayout
datos=[]


TAB_OBJETIVOS=1
tuplas_tablas=[
    (Ciclo,"nombre"), (Curso, "nombre_curso"), (Modulo, "nombre"),
]


    
    
class FabricaTabs(object):
    @staticmethod
    def get_tab_objetivos(texto_tab, ciclo_id):
        tab=TabbedPanelHeader(text=texto_tab)
        tab.content=Button(text=texto_tab)
        return tab
    @staticmethod
    def get_representacion_objetivo_general(objetivos):
        
        lista_cadenas=[]
        for o in objetivos:
            lista_cadenas.append(o.letra+") "+o.texto)
        return lista_cadenas
        
    @staticmethod
    def get_representacion(modelos):
        if isinstance(modelos[0],  ObjetivoGeneral):
            lista_cadenas=FabricaTabs.get_representacion_objetivo_general(modelos)
        caja=BoxLayout(orientation="vertical")
        for cadena in lista_cadenas:
            b=ToggleButton(text=cadena)
            caja.add_widget(b)
        return caja
            
        
    
class GuiApp(App):        
    def get_cadenas(modelos, tupla_configuracion):
        lista_textos=[]
        for m in modelos:
            lista_textos.append(m.__dict__[tupla_configuracion[1]])
        return lista_textos


    def on_ciclo_seleccionado(self, boton):
        ciclo_seleccionado=self.todos_ciclos.get(nombre=boton.text)
        print(ciclo_seleccionado)
        self.crear_botones_cursos(ciclo_seleccionado)
        self.rellenar_objetivos_generales(ciclo_seleccionado)
    
    def rellenar_objetivos_generales(self, ciclo_seleccionado):
        objetivos=self.todos_objetivos_generales.filter(ciclo=ciclo_seleccionado)
        print(objetivos)
        caja_controles=FabricaTabs.get_representacion(objetivos)
        self.root.ids.tab_objetivos.clear_widgets()
        self.root.ids.tab_objetivos.content=caja_controles
        
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
        ciclos=self.todos_ciclos
        for ciclo in ciclos:
            #btn_ciclo=Button(text=ciclo, height=45)
            btn_ciclo=ToggleButton(text=ciclo.nombre, height=45, group="ciclos", shorten=True)
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
    
    
        
        
    def on_start(self):
        self.todos_objetivos_generales  =   ObjetivoGeneral.objects.all()
        self.todos_ciclos               =   Ciclo.objects.all()
        self.todos_cursos               =   Curso.objects.all()
        self.todos_modulos              =   Modulo.objects.all()
        
        self.crear_botones_ciclos()
        
        #Cambiamos el texto del tab por defecto
        self.root.ids.tabs.default_tab_text = 'Objetivos generales'
        return 
        
        

if __name__ == '__main__':
    GuiApp().run()
    
    
    