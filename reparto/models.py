from django.db import models
from django.forms import ModelForm
from gestionbd.models import Modulo
# Create your models here.



class Reparto ( models.Model ):
    nombre=models.CharField(max_length=30)
    
class RepartoForm ( ModelForm ):
    class Meta:
        model=Reparto
        fields=["nombre"]
    
class Profesor ( models.Model ):
    nombre = models.CharField( max_length=20 )
    posicion = models.IntegerField()
    
    
class ModuloParaRepartir ( models.Model ):
    reparto     = models.ForeignKey ( Reparto )
    modulo      = models.ForeignKey ( Modulo )
    asignado    = models.ForeignKey (Profesor, blank=True )
    
class Asignacion ( models.Model ):
    profesor    = models.ForeignKey ( Profesor )
    reparto     = models.ForeignKey ( Reparto )