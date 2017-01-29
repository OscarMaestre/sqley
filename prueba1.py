#!/usr/bin/env python3


from tkinter import *


def get_boton(texto, padre):
    btn=Button(padre, text=texto)
    return btn

def get_btn_izq(texto, padre):
    return get_boton(texto, padre).pack(side=LEFT)

def get_btn_der(texto, padre):
    return get_boton(texto, padre).pack(side=RIGHT)

def main():
    ventana=Tk()
    frame1=Frame(ventana, background="blue")
    frame1.pack()
    
    frame2=Frame(ventana, background="red")
    frame2.pack(fill=BOTH, expand=True)
    Button(frame1, text="Boton 1").pack()
    Button(frame1, text="Boton 2").pack()
    
    Button(frame2, text="Boton 3").pack(side=LEFT, fill=Y, expand=True)
    Button(frame2, text="Boton 4").pack(side=LEFT)
    Button(frame2, text="Boton 5").pack(side=LEFT, fill=Y, expand=True)
    
    ventana.mainloop()
    
    
if __name__ == '__main__':
    main()