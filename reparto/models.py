from django.db import models
from django.forms import ModelForm
from gestionbd.models import Profesor
# Create your models here.



class Reparto ( models.Model ):
    nombre=models.CharField(max_length=30)
    
class RepartoForm ( ModelForm ):
    class Meta:
        model=Reparto
        fields=["nombre"]
    
    
class ModuloEnReparto ( models.Model ):
    nombre          =   models.CharField ( max_length=140 )
    grupo           =   models.CharField ( max_length=20 )
    horas_semanales =   models.IntegerField()
    especialidad    =   models.CharField(max_length=10)
    def __str__(self ):
        return self.nombre + "("+ str(self.curso) + ")"
    
class ModuloPorAsignar ( models.Model ):
    modulo      = models.ForeignKey ( ModuloEnReparto )
    reparto     = models.ForeignKey ( Reparto )
    
class ModuloAsignado ( models.Model ):
    modulo      = models.ForeignKey ( ModuloEnReparto )
    reparto     = models.ForeignKey ( Reparto )
    profesor    = models.ForeignKey ( Profesor )
    
