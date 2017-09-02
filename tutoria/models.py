from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import SelectDateWidget
from gestionbd.models import Curso, Modulo

# Create your models here.


class Alumno(models.Model):
    ESTADOS_INDENPENDENCIA=[
        ("EMANCIPADO", "Estoy independizado"),
        ("NO_EMANCIPADO", "No estoy independizado")
    ]
    apellido1           =   models.CharField(max_length=60)
    apellido2           =   models.CharField(max_length=60)
    nombre              =   models.CharField(max_length=40)
    
    dni                 =   models.CharField(max_length=10)
    
    fecha_nacimiento    =   models.DateField()
    
    tutor1              =   models.CharField(max_length=80)
    tutor2              =   models.CharField(max_length=80)
    
    independizado       =   models.CharField(choices=ESTADOS_INDENPENDENCIA, max_length=100)
    calle_notas         =   models.CharField(max_length=80)
    cp_notas            =   models.IntegerField(default=13001)
    poblacion_notas     =   models.CharField(max_length=40, default="Ciudad Real")
    
    tlf_alumno          =   models.CharField(max_length=14)
    tlf_urgencia        =   models.CharField(max_length=14)
    foto                =   models.FileField()
    
    repetidor           =   models.BooleanField()
    
    curso               =   models.ForeignKey(Curso)
    
    
class Matricula(models.Model):
    SITUACIONES=(
        ("APRO",        "Lo tengo aprobado de años anteriores")  ,
        ("CONV",        "Lo tengo convalidado"),
        ("PEND CONV.",  "Quiero pedir que me lo convaliden") ,
        ("MATRICULADO", "Tengo que cursarlo"),
    )
    alumno              =   models.ForeignKey(Alumno)
    modulo              =   models.ForeignKey(Modulo)
    situacion           =   models.CharField (max_length=10,
                                              choices=SITUACIONES)
    convocatorias_restantes=models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )