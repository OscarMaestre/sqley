#!/usr/bin/env python3

from tkinter import *
from tkinter.ttk import *
from time import sleep

import sys, os, importlib

filename=".."+os.path.sep+"graficos"+os.path.sep+"ConfiguradorGrid.py"
sys.path.append(os.path.dirname(filename))
mname = os.path.splitext(os.path.basename(filename))[0]
imported = importlib.import_module("ConfiguradorGrid")                       
sys.path.pop()

from ConfiguradorGrid import ConfiguradorGrid

class TestConfigurador(object):
    def __init__(self, padre):
        self.padre=padre
        self.padding_x=10
        self.padding_y=10
        self.pausa=0.1
        
    def buildUI(self):
        pesos_filas=[1, 4]
        pesos_columnas=[4,1]
        ConfiguradorGrid.configurar_grid(
            self.padre,pesos_filas, pesos_columnas)
        
        self.crear_boton(self.padre, 0, 0, "B1")
        self.crear_boton(self.padre, 0, 1, "B2")
        self.crear_boton(self.padre, 1, 0, "B3")
        self.crear_boton(self.padre, 1, 1, "B4")
        
        self.canvas=Canvas(self.padre, bg="green")
        self.canvas.grid(row=2, column=0, columnspan=2,
                    padx=self.padding_x, pady=self.padding_y,
                    sticky=N+S+E+W)
        
        
    def crear_boton(self, padre, fila, columna, texto):
        btn=Button(padre, text=texto)
        btn.grid(row=fila, column=columna, sticky=N+S+E+W,
                 padx=self.padding_x,
                 pady=self.padding_y)
        btn.bind("<ButtonRelease-1>", self.dibujar)
        return btn
        
    def dibujar(self, evento):
        for i in range(0, 100):
            sleep(self.pausa)
            self.canvas.create_line(0, i, 200, i)
            self.canvas.update()
            
    
if __name__ == '__main__':
    Ventana=Tk()
    test=TestConfigurador(Ventana)
    test.buildUI()
    Ventana.wm_attributes("-zoomed",1)
    Ventana.mainloop()