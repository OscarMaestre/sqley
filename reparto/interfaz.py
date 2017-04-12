#!/usr/bin/env python3

import wx
from wx import xrc

class Reparto(wx.App):
    def OnInit(self):
        self.recursos = xrc.XmlResource("interfaz.xrc")
        self.inicializar()
        self.crearPanelProfesor("Pepe")
        return True
    
    def inicializar(self):
        self.ventana_principal=self.recursos.LoadFrame(None, "VentanaPrincipal")
        self.sizerProfesores=xrc.XRCCTRL(self.ventana_principal, "sizerGlobal")
        print(self.sizerProfesores)
        self.ventana_principal.Show()
        
        
        
    def crearPanelProfesor(self, nombre):
        recursoPanelProfesor=xrc.XmlResource("panelProfesor.xrc")
        
        panelProfesor=recursoPanelProfesor.LoadPanel(self.ventana_principal, "panelProfesor")
        txtNombreProfesor=xrc.XRCCTRL(panelProfesor, "txtNombreProfesor")
        txtNombreProfesor.SetLabel(nombre)
        
        txtHorasProfesor=xrc.XRCCTRL(panelProfesor, "txtHorasProfesor")
        txtHorasProfesor.SetLabel("0 horas")
        
        
        
if __name__ == '__main__':
    aplicacion=Reparto(False)
    aplicacion.MainLoop()