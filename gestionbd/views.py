from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import *
# Create your views here.


control="""
<input type="text" value="{0}" size="130" onclick="this.select();document.execCommand('copy');">
"""

def get_objetivos_generales_html(ciclo_pasado):
    resultado="<h3>Objetivos generales</h3>"
    competencias=ObjetivoGeneral.objects.filter(ciclo=ciclo_pasado)
    for c in competencias:
        resultado+=control.format(c.texto)
    return resultado



def get_competencias_html(ciclo_pasado):
    resultado="<h3>Competencias profesionales</h3>"
    competencias=Competencia.objects.filter(ciclo=ciclo_pasado)
    for c in competencias:
        resultado+=control.format(c.texto)
    return resultado


def get_competencias_generales_html(ciclo_pasado):
    resultado="<h3>Competencias generales</h3>"
    competencias=CompetenciaGeneral.objects.filter(ciclo=ciclo_pasado)
    for c in competencias:
        resultado+=control.format(c.texto)
    return resultado



def get_cualificaciones_profesionales_html(ciclo_pasado, completas):
    if completas:
        resultado="<h3>Cualificaciones profesionales completas</h3>"
    else:
        resultado="<h3>Cualificaciones profesionales incompletas</h3>"
    ciclo_cuali=CicloTieneCualificacion.objects.filter(
        ciclo=ciclo_pasado, es_completa=completas
    )
    
    for c in ciclo_cuali:
        resultado+=control.format(c.cualificacion_profesional.texto)
    return resultado


def get_resultados_aprendizaje_html(modulo):
    resultado="<h3>Resultados de aprendizaje</h3>"
    competencias=ResultadoDeAprendizaje.objects.filter(modulo=modulo_pasado)
    for c in competencias:
        resultado+=control.format(c.texto)
    return resultado

def get_elementos_html(ciclo_pasado):
    resultado="<h1>{0}</h1>".format(ciclo_pasado.nombre)
    resultado+=get_objetivos_generales_html(ciclo_pasado)
    resultado+=get_competencias_generales_html(ciclo_pasado)
    resultado+=get_competencias_html(ciclo_pasado)
    resultado+=get_cualificaciones_profesionales_html(ciclo_pasado, completas=True)
    resultado+=get_cualificaciones_profesionales_html(ciclo_pasado, completas=False)
    resultado+=get_competencias_html(ciclo_pasado)
    return resultado

def get_datos_modulo(modulo):
    resultado="<h3>"+modulo.nombre+"</h3>"
    resultado+=get_contenidos_modulo(modulo)
    resultado+=get_resultados_aprendizaje_modulo(modulo)
    return resultado

def get_contenidos_modulo(modulo_pasado):
    resultado="<h3>Contenidos para {0}</h3>".format(modulo_pasado.nombre)
    contenidos=Contenido.objects.filter(modulo=modulo_pasado)
    for c in contenidos:
        resultado+=control.format(str(c.numero) + ") " + c.texto)
    return resultado


def get_resultados_aprendizaje_modulo(modulo_pasado):
    resultado="<h3>Resultados de aprendizaje para {0}</h3>".format(modulo_pasado.nombre)
    resultados_aprendizaje=ResultadoDeAprendizaje.objects.filter(modulo=modulo_pasado)
    for ra in resultados_aprendizaje:
        resultado+=control.format(str(ra.numero) + ") " + ra.texto)
        crit_evaluacion=CriterioDeEvaluacion.objects.filter(
            resultado_de_aprendizaje=ra
        )
        resultado+="<h4>Criterios para {0}</h4>".format(ra.texto)
        for ce in crit_evaluacion:
            resultado+=control.format(ce.letra+") "+ce.texto)
        
    return resultado

def cortar_elementos ( peticion ):
    ciclo=Ciclo.objects.all().order_by("nombre");
    resultado=""
    for c in ciclo:
        resultado+=get_elementos_html(c)
        cursos=Curso.objects.filter(ciclo=c).order_by("num_curso")
        for cu in cursos:
            modulos=Modulo.objects.filter(curso=cu).order_by("nombre")
            for modulo in modulos:
                resultado+=get_datos_modulo(modulo)
        
    return HttpResponse(content=resultado)
        