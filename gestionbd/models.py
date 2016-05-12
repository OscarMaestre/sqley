from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Ciclo( models.Model ):
    nombre      =   models.CharField ( max_length=140 )
    abreviatura =   models.CharField ( max_length=10 )
    class Meta:
        db_table="ciclos"

class Modulo( models.Model ):
    nombre          =   models.CharField ( max_length=140 )
    codigo_junta    =   models.IntegerField()
    horas_anuales   =   models.IntegerField()
    horas_semanales =   models.IntegerField()
    ciclo           =   models.ForeignKey ( Ciclo )
    class Meta:
        db_table="modulos"
        
class ResultadoDeAprendizaje ( models.Model ):
    texto       =   models.CharField ( max_length=250 )
    numero      =   models.IntegerField()
    modulo      =   models.ForeignKey ( Modulo )
    class Meta:
        db_table="resultados_de_aprendizaje"
        
class CriterioDeEvaluacion ( models.Model ):
    texto                       =   models.CharField ( max_length=250 )
    letra                       =   models.CharField ( max_length= 2)
    resultado_de_aprendizaje    =   models.ForeignKey ( ResultadoDeAprendizaje )
    class Meta:
        db_table="criterios_de_evaluacion"
        
class Contenido ( models.Model ):
    texto       =   models.CharField ( max_length=250 )
    numero      =   models.IntegerField()
    modulo      =   models.ForeignKey ( Modulo )
    class Meta:
        db_table="contenidos"
        
class PuntoDeContenido ( models.Model ):
    texto       =   models.CharField ( max_length=250 )
    contenido   =   models.ForeignKey ( Contenido )
    
    class Meta:
        db_table="puntos_de_contenidos"