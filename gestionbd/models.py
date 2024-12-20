from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Ciclo( models.Model ):
    nombre              =   models.CharField ( max_length=140 )
    abreviatura         =   models.CharField ( max_length=10 )
    nivel_profesional   =   models.IntegerField()
    num_decreto_jccm    =   models.IntegerField()
    fecha_decreto_jccm  =   models.DateField()
    num_decreto_boe     =   models.IntegerField()
    fecha_decreto_boe   =   models.DateField()
    
    def __str__(self ):
        return self.abreviatura
    
    class Meta:
        db_table="ciclos"

class Curso( models.Model ):
    num_curso           = models.IntegerField()
    nombre_curso        = models.CharField ( max_length = 20 )
    ciclo               = models.ForeignKey ( Ciclo , on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_curso
    class Meta:
        db_table="cursos"
        
class Grupo ( models.Model ):
    nombre_grupo    =   models.CharField(max_length=15)
    curso           =   models.ForeignKey ( Curso , on_delete=models.CASCADE )
    def __str__(self):
        return self.nombre_grupo
    class Meta:
        db_table="grupos"
        
class EspecialidadProfesor ( models.Model ):
    ESPECIALIDADES = [ ("PS", "Prof. Secundaria"),
                        ("PT", "Prof. Tecnico") ,
                        ("TODAS", "Todas las esp.")]
    especialidad = models.CharField ( max_length = 30, choices = ESPECIALIDADES )
    def __str__(self):
        return self.especialidad
    class Meta:
        db_table="especialidesprofesorado"
        verbose_name_plural = "Especialidades"
        
class Profesor ( models.Model ):
    nombre = models.CharField( max_length = 20 )
    horas_minimas = models.IntegerField()
    num_posicion=models.IntegerField()
    especialidad = models.ForeignKey ( EspecialidadProfesor  , on_delete=models.CASCADE)
    def to_java(self):
        inicializacion_java="""
        Profesor m{0} = new Profesor({0}, {1}, {2},\"{3}\", \"{4}\")""".format(self.id, self.nombre, self.horas_minimas)
        return inicializacion_java
    def __str__(self):
        return self.nombre
    class Meta:
        db_table="profesores"
        verbose_name_plural = "Profesores"
        
class Modulo( models.Model ):
    nombre          =   models.CharField ( max_length=140 )
    codigo_junta    =   models.CharField ( max_length=5   )
    horas_anuales   =   models.IntegerField()
    horas_semanales =   models.IntegerField()
    curso           =   models.ForeignKey(Curso , on_delete=models.CASCADE)
    especialidad    =   models.CharField(max_length=10)
    def __str__(self ):
        return self.nombre + "("+ str(self.curso) + ")"
    
    def to_java(self, nombre_vector,indice):
        inicializacion_java="""
        Modulo m{0} = new Modulo({0}, {1}, {2},\"{3}\", \"{4}\");""".format(self.id, self.codigo_junta, self.horas_semanales, self.nombre,str(self.curso))
        inicializacion_java+="\n\t\t{0}[{1}]=m{2}".format(nombre_vector, indice, self.id)
        return inicializacion_java.strip()
        
    def to_python(self, nombre_vector, indice):
        construccion="ModuloLeido ( {0}, {1},    {2},    \"{3}\",    \"{4}\")".format(self.id, self.codigo_junta, self.horas_semanales, self.nombre,str(self.curso))
        inicializacion_python="\n        {0}.append({1})".format(nombre_vector,construccion, indice, self.id)
        return inicializacion_python
    
    class Meta:
        db_table="modulos"
        verbose_name_plural = "Modulos"
        ordering = ["nombre", "curso"]


class Competencia ( models.Model):
    identificador   = models.CharField(max_length=2)
    texto           = models.CharField (max_length=240)
    ciclo           = models.ForeignKey ( Ciclo  , on_delete=models.CASCADE)
    def __str__(self):
        return self.ciclo.abreviatura + " " + self.texto
    class Meta:
        db_table="competencias"
        verbose_name_plural = "Competencias"
    
class CompetenciaGeneral ( models.Model ):
    texto           = models.CharField (max_length=512)
    ciclo           = models.ForeignKey ( Ciclo  , on_delete=models.CASCADE)
    def __str__(self):
        return self.texto
    class Meta:
        db_table="competenciasgenerales"
        verbose_name_plural = "Competencias Generales"
    
class CualificacionProfesional ( models.Model ):
    identificador   =   models.CharField(max_length=2)
    texto           =   models.CharField (max_length=240 )
    ciclo           =   models.ManyToManyField ( Ciclo, through="CicloTieneCualificacion" )
    real_decreto    =   models.CharField (max_length=240)
    def __str__(self):
        return self.texto
    class Meta:
        db_table="cualificaciones_profesionales"
        verbose_name_plural = "Cualificaciones profesionales"
        
class CicloTieneCualificacion ( models.Model ):
    ciclo = models.ForeignKey(Ciclo , on_delete=models.CASCADE)
    cualificacion_profesional = models.ForeignKey ( CualificacionProfesional  , on_delete=models.CASCADE)
    es_completa = models.BooleanField()
    def __str__(self):
        return self.cualificacion_profesional.identificador + str(self.es_completa)
    class Meta:
        db_table="ciclo_tiene_cualificacion"
        verbose_name_plural = "Ciclo y cualificaciones"
        

class UnidadDeCompetencia ( models.Model ):
    identificador   =   models.CharField(max_length=2)
    texto           =   models.CharField (max_length=240 )
    cualificacion   =   models.ManyToManyField ( CualificacionProfesional )
    def __str__(self):
        return self.texto
    class Meta:
        db_table="unidades_de_competencia"
        verbose_name_plural = "Unidades de competencia"
    
class ResultadoDeAprendizaje ( models.Model ):
    texto       =   models.CharField ( max_length=250 )
    numero      =   models.IntegerField()
    modulo      =   models.ForeignKey ( Modulo  , on_delete=models.CASCADE)
    def __str__(self ):
        return self.texto + "("+str (self.modulo) + ")"
    class Meta:
        db_table="resultados_de_aprendizaje"
        verbose_name_plural = "Resultados de aprendizaje"
        
class CriterioDeEvaluacion ( models.Model ):
    texto                       =   models.CharField ( max_length=250 )
    letra                       =   models.CharField ( max_length= 2)
    resultado_de_aprendizaje    =   models.ForeignKey ( ResultadoDeAprendizaje  , on_delete=models.CASCADE)
    def __str__(self ):
        cod_curso=self.resultado_de_aprendizaje.modulo.curso.nombre_curso
        return cod_curso+") " + self.texto
    class Meta:
        db_table="criterios_de_evaluacion"
        verbose_name_plural = "Criterios de evaluacion"
        
class Contenido ( models.Model ):
    texto       =   models.CharField ( max_length=250 )
    numero      =   models.IntegerField()
    modulo      =   models.ForeignKey ( Modulo  , on_delete=models.CASCADE)
    def __str__(self ):
        return self.texto + "("+str (self.modulo) + ")"
    class Meta:
        db_table="contenidos"
        
class ObjetivoGeneral ( models.Model ):
    letra   =   models.CharField(max_length=2)
    texto   =   models.CharField(max_length=2048)
    ciclo   =   models.ForeignKey ( Ciclo  , on_delete=models.CASCADE)
    def __str__(self):
        return self.ciclo.abreviatura + " " + self.letra + ") " + self.texto
    class Meta:
        db_table="objetivosgenerales"
        verbose_name_plural = "Objetivos Generales de Ciclo"
        
class PuntoDeContenido ( models.Model ):
    texto       =   models.CharField ( max_length=250 )
    num_orden   =   models.IntegerField()
    contenido   =   models.ForeignKey ( Contenido  , on_delete=models.CASCADE)
    def __str__(self ):
        return self.texto
    class Meta:
        db_table="puntos_de_contenidos"
        verbose_name_plural = "Puntos de contenido"