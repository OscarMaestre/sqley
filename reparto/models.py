from django.db import models

from gestionbd.models import Modulo
# Create your models here.



class Reparto ( models.Model ):
    nombre=models.TextField(max_length=40)
    
    
class Profesor ( models.Model ):
    nombre = models.TextField(max_length=40)
    
    
class ModuloParaRepartir ( models.Model ):
    reparto     = models.ForeignKey ( Reparto )
    modulo      = models.ForeignKey ( Modulo )
    asignado    = models.ForeignKey (Profesor, blank=True )
    
class Asignacion ( models.Model ):
    profesor    = models.ForeignKey ( Profesor )
    reparto     = models.ForeignKey ( Reparto )