#!/usr/bin/env python

import wx
from wx import xrc

class Reparto(wx.App):
    def OnInit(self):
        self.recursos = xrc.XmlResource("interfaz.xrc")
        self.inicializar()
        return True
    
    def inicializar(self):
        self.ventana_principal=self.recursos.LoadFrame(None, "VentanaPrincipal")
        self.ventana_principal.Show()
        
        
if __name__ == '__main__':
    aplicacion=Reparto(False)
    aplicacion.MainLoop()