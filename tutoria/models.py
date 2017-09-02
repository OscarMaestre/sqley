from django.db import models

# Create your models here.


class Alumno(models.Model):
    apellido1           =   models.CharField(max_length=60)
    apellido2           =   models.CharField(max_length=60)
    nombre              =   models.CharField(max_length=40)
    
    dni                 =   models.CharField(max_length=10)
    
    fecha_nacimiento    =   models.DateField()
    
    tutor1              =   models.CharField(max_length=80)
    tutor2              =   models.CharField(max_length=80)
    
    vive_solo           =   models.BooleanField()
    calle_notas         =   models.CharField(max_length=80)
    cp_notas            =   models.IntegerField()
    poblacion_notas     =   models.CharField(max_length=40)
    
    tlf_alumno          =   models.CharField(max_length=14)
    tlf_urgencia        =   models.CharField(max_length=14)
    
    
    
    