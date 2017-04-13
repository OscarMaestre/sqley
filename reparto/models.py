from django.db import models
from django.forms import ModelForm
from gestionbd.models import Profesor, Modulo
# Create your models here.



class Reparto ( models.Model ):
    nombre=models.CharField(max_length=30)
    
class RepartoForm ( ModelForm ):
    class Meta:
        model=Reparto
        fields=["nombre"]
    
    
    
class Asignacion (models.Model):
    reparto     =   models.ForeignKey(Reparto)
    profesor    =   models.ForeignKey(Profesor)
    modulo      =   models.ForeignKey(Modulo)
