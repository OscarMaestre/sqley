from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Ciclo( models.Model ):
    nombre      =   models.CharField ( max_length=140 )
    abreviatura =   models.CharField ( max_length=10 )
    def __str__(self ):
        return self.abreviatura
    
    class Meta:
        db_table="ciclos"

class Curso( models.Model ):
    num_curso    = models.IntegerField()
    nombre_curso = models.CharField ( max_length = 20 )
    ciclo        = models.ForeignKey ( Ciclo )
    def __str__(self):
        return self.nombre_curso
    class Meta:
        db_table="cursos"
        
class Grupo ( models.Model ):
    nombre_grupo    =   models.CharField(max_length=15)
    curso           =   models.ForeignKey ( Curso )
    class Meta:
        db_table="grupos"
        
class Reparto ( models.Model ):
    nombre_reparto = models.CharField( max_length= 20 )
    class Meta:
        db_table="repartos"
        
class Profesor ( models.Model ):
    nombre = models.CharField( max_length = 20 )
    horas_minimas = models.IntegerField()
    def to_java(self):
        inicializacion_java="""
        Profesor m{0} = new Profesor({0}, {1}, {2},\"{3}\", \"{4}\")""".format(self.id, self.nombre, self.horas_minimas)
        return inicializacion_java
    class Meta:
        db_table="profesores"
        
class Modulo( models.Model ):
    nombre          =   models.CharField ( max_length=140 )
    codigo_junta    =   models.IntegerField()
    horas_anuales   =   models.IntegerField()
    horas_semanales =   models.IntegerField()
    curso           =   models.ForeignKey(Curso)
    especialidad    =   models.CharField(max_length=10)
    def __str__(self ):
        return self.nombre + "("+ str(self.curso) + ")"
    
    def to_java(self, nombre_vector,indice):
        inicializacion_java="""
        Modulo m{0} = new Modulo({0}, {1}, {2},\"{3}\", \"{4}\");""".format(self.id, self.codigo_junta, self.horas_semanales, self.nombre,str(self.curso))
        inicializacion_java+="\n\t\t{0}[{1}]=m{2}".format(nombre_vector, indice, self.id)
        return inicializacion_java.strip()
        
    class Meta:
        db_table="modulos"
        
class ResultadoDeAprendizaje ( models.Model ):
    texto       =   models.CharField ( max_length=250 )
    numero      =   models.IntegerField()
    modulo      =   models.ForeignKey ( Modulo )
    def __str__(self ):
        return self.texto + "("+str (self.modulo) + ")"
    class Meta:
        db_table="resultados_de_aprendizaje"
        
class CriterioDeEvaluacion ( models.Model ):
    texto                       =   models.CharField ( max_length=250 )
    letra                       =   models.CharField ( max_length= 2)
    resultado_de_aprendizaje    =   models.ForeignKey ( ResultadoDeAprendizaje )
    def __str__(self ):
        return self.texto
    class Meta:
        db_table="criterios_de_evaluacion"
        
class Contenido ( models.Model ):
    texto       =   models.CharField ( max_length=250 )
    numero      =   models.IntegerField()
    modulo      =   models.ForeignKey ( Modulo )
    def __str__(self ):
        return self.texto + "("+str (self.modulo) + ")"
    class Meta:
        db_table="contenidos"
        
class PuntoDeContenido ( models.Model ):
    texto       =   models.CharField ( max_length=250 )
    num_orden   =   models.IntegerField()
    contenido   =   models.ForeignKey ( Contenido )
    def __str__(self ):
        return self.texto
    class Meta:
        db_table="puntos_de_contenidos"