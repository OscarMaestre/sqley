#!/usr/bin/env python3

class ConfiguradorGrid(object):
    @staticmethod
    def configurar_grid(control, filas, columnas):
        for fila, peso in enumerate(filas):
            control.grid_rowconfigure(fila, weight=peso)
            
        for columna, peso in enumerate(columnas):
            control.grid_columnconfigure(columna, weight=peso)
            

