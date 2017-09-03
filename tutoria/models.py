from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.forms import SelectDateWidget
from gestionbd.models import Curso, Modulo

# Create your models here.


class Alumno(models.Model):
    ESTADOS_INDENPENDENCIA=[
        ("EMANCIPADO", "Estoy independizado"),
        ("NO_EMANCIPADO", "No estoy independizado")
    ]

    regex_validador_dni =   "([0-9]{7,8}[A-Z])|([A-Z][0-9]{7,8})"
    mensaje_error_dni   =   "En el DNI/NIE por favor, usa solo numeros y mayúsculas. Ni guiones, ni puntos ni cualquier otro símbolo, gracias"
    validador_dni       =   RegexValidator(regex=regex_validador_dni,
                                           message=mensaje_error_dni)
    apellido1           =   models.CharField(max_length=60)
    apellido2           =   models.CharField(max_length=60)
    nombre              =   models.CharField(max_length=40)
    
    dni                 =   models.CharField(max_length=10,
                                validators=[validador_dni],
                                primary_key=True)
    
    email               =   models.EmailField()
    fecha_nacimiento    =   models.DateField()
    
    tutor1              =   models.CharField(max_length=80)
    tutor2              =   models.CharField(max_length=80)
    
    independizado       =   models.CharField(choices=ESTADOS_INDENPENDENCIA, max_length=100)
    direccion_notas     =   models.CharField(max_length=80)
    cp_notas            =   models.IntegerField(default=13001)
    poblacion_notas     =   models.CharField(max_length=40, default="Ciudad Real")
    
    tlf_alumno          =   models.CharField(max_length=14)
    tlf_urgencia        =   models.CharField(max_length=14)
    foto                =   models.FileField()
    
    repetidor           =   models.BooleanField()
    
    curso               =   models.ForeignKey(Curso)
    
    def __str__(self):
        return self.apellido1 + " " + self.apellido2 + " "+self.nombre
    
    
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
                                              choices=SITUACIONES,
                                              default="MATRICULADO")
    convocatorias_restantes=models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
        default=4
    )