from django.db import models
from gestionbd.models import Modulo, CriterioDeEvaluacion
# Create your models here.



class PuntoMetodologico(models.Model):
    texto = models.CharField(max_length=4096)
    
    class Meta:
        db_table="puntos_de_metodologia"
        verbose_name_plural = "Puntos de Metodologia"
        
    def __str__(self):
        return self.texto


class Evaluacion(models.Model):
    numero          =   models.IntegerField()
    fecha_inicio    =   models.DateField()
    fecha_fin       =   models.DateField()
    def __str__(self):
        return "Evaluacion " + str(self.numero)
    class Meta:
        db_table="evaluaciones"
        verbose_name_plural = "Evaluaciones"
        
class RecursoDidactico(models.Model):
    nombre      =   models.CharField(max_length=250)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table="recursos_didacticos"
        verbose_name_plural = "Recursos didacticos"
        
class InstrumentoEvaluacion(models.Model):
    nombre      =   models.CharField(max_length=250)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table="instrumentos_evaluacion"
        verbose_name_plural = "Instrumentos de evaluacion"
        
class ProcedimientoEvaluacion(models.Model):
    nombre      =   models.CharField(max_length=250)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table="procedimientosevaluacion"
        verbose_name_plural = "Procedimientos de evaluacion"
        
class UnidadDeTrabajo(models.Model):
    numero              = models.IntegerField()
    nombre              = models.CharField(max_length=180)
    sesiones            = models.IntegerField()
    puntos_metodologia  = models.ManyToManyField(PuntoMetodologico)
    evaluaciones        = models.ManyToManyField(Evaluacion)
    recursos            = models.ManyToManyField(RecursoDidactico)
    instrumentos        = models.ManyToManyField(InstrumentoEvaluacion)
    procedimientos      = models.ManyToManyField(ProcedimientoEvaluacion)
    criterios           = models.ManyToManyField(CriterioDeEvaluacion, through="Interviene")
    class Meta:
        db_table="unidades_de_trabajo"
        verbose_name_plural = "Unidades de Trabajo"
        
    def __str__(self):
        return self.nombre

class Calificador(models.Model):
    texto              = models.CharField(max_length=180)
    class Meta:
        db_table="calificadores"
        verbose_name_plural = "Calificadores"

#Usado para indicar que en una unidad de trabajo
#intervienen uno o mas criterios de evaluacion
#y que un criterio se puede usar en muchas unidades
class Interviene(models.Model):
    criterio = models.ForeignKey(CriterioDeEvaluacion, on_delete=models.CASCADE)
    unidad_de_trabajo = models.ForeignKey ( UnidadDeTrabajo, on_delete=models.CASCADE )
    es_criterio_minimo = models.BooleanField()
    ponderacion = models.IntegerField()
    calificador = models.ForeignKey ( Calificador, on_delete = models.CASCADE )
    class Meta:
        db_table="criterios_unidades_trabajo"
        verbose_name_plural = "Criterios en UT"
        
class Programacion(models.Model):
    nombre      =   models.CharField(max_length=240)
    modulo      =   models.ManyToManyField ( Modulo )
    unidades    =   models.ManyToManyField ( UnidadDeTrabajo )
    class Meta:
        db_table="programaciones"
        verbose_name_plural = "Programaciones"