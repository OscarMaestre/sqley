from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.http import HttpResponse
from .models import *
# Create your views here.


control="""
<input type="text" value="{0}" size="135"
    onfocus="this.select();document.execCommand('copy');">
"""

def get_objetivos_generales_html(ciclo_pasado):
    resultado="<h2>Objetivos generales del ciclo</h2>"
    competencias=ObjetivoGeneral.objects.filter(ciclo=ciclo_pasado)
    for c in competencias:
        resultado+=control.format(c.texto)
    return resultado



def get_competencias_html(ciclo_pasado):
    resultado="<h2>Competencias profesionales, pers y sociales del ciclo</h2>"
    competencias=Competencia.objects.filter(ciclo=ciclo_pasado)
    for c in competencias:
        resultado+=control.format(c.texto)
    return resultado


def get_competencias_generales_html(ciclo_pasado):
    resultado="<h2>Competencias generales del ciclo</h2>"
    competencias=CompetenciaGeneral.objects.filter(ciclo=ciclo_pasado)
    for c in competencias:
        resultado+=control.format(c.texto)
    return resultado


def get_unidades_competencia_asociadas(cualificacion):
    pass

def get_cualificaciones_profesionales_html(ciclo_pasado, completas):
    if completas:
        resultado="<h2>Cualificaciones profesionales completas del ciclo</h2>"
    else:
        resultado="<h2>Cualificaciones profesionales incompletas del ciclo</h2>"
    ciclo_cuali=CicloTieneCualificacion.objects.filter(
        ciclo=ciclo_pasado, es_completa=completas
    )
    
    for c in ciclo_cuali:
        resultado+=control.format(c.cualificacion_profesional.identificador +
                                  ") " + c.cualificacion_profesional.texto)
    return resultado


def get_resultados_aprendizaje_html(modulo):
    resultado="<h3>Resultados de aprendizaje</h3>"
    competencias=ResultadoDeAprendizaje.objects.filter(modulo=modulo_pasado)
    for c in competencias:
        resultado+=control.format(c.texto)
    return resultado

def get_elementos_html(ciclo_pasado):
    resultado="<h2>{0}</h2>".format(ciclo_pasado.nombre)
    resultado+=get_objetivos_generales_html(ciclo_pasado)
    resultado+=get_competencias_generales_html(ciclo_pasado)
    resultado+=get_competencias_html(ciclo_pasado)
    resultado+=get_cualificaciones_profesionales_html(ciclo_pasado, completas=True)
    resultado+=get_cualificaciones_profesionales_html(ciclo_pasado, completas=False)
    resultado+=get_competencias_html(ciclo_pasado)
    return resultado

def get_datos_modulo(modulo):
    c=modulo.curso.ciclo
    resultado=""
    
    resultado+="<h1>"+modulo.nombre+"</h1>"
    resultado+=get_elementos_html(c)
    resultado+=get_contenidos_modulo(modulo)
    resultado+=get_resultados_aprendizaje_modulo(modulo)
    resultado+=get_resultados_aprendizaje_modulo_tabla(modulo)
    return resultado

def get_contenidos_modulo(modulo_pasado):
    resultado="<h3>Contenidos para {0}</h3>".format(modulo_pasado.nombre)
    contenidos=Contenido.objects.filter(modulo=modulo_pasado)
    for c in contenidos:
        resultado+="<hr/>Contenido general<br/>"
        #resultado+=control.format(str(c.numero) + ") " + c.texto)
        resultado+=control.format(c.texto)
        resultado+=get_punto_contenido ( c )
    return resultado

def get_punto_contenido(contenido_pasado):
    resultado="<h4>Puntos de contenido para {0}) {1}</h4>".format(
        str(contenido_pasado.numero), contenido_pasado.texto
    )
    puntos_contenido=PuntoDeContenido.objects.filter(
        contenido=contenido_pasado).order_by("num_orden")
    for p in puntos_contenido:
        resultado+=control.format(
            p.texto
        )
    return resultado

def get_resultados_aprendizaje_modulo(modulo_pasado):
    resultado="<h3>Resultados de aprendizaje para {0}</h3>".format(modulo_pasado.nombre)
    resultados_aprendizaje=ResultadoDeAprendizaje.objects.filter(modulo=modulo_pasado)
    
    for ra in resultados_aprendizaje:
        resultado+="<hr/><h4>Resultado</h4>"
        #resultado+=control.format(str(ra.numero) + ") " + ra.texto)
        resultado+=control.format(ra.texto)
        crit_evaluacion=CriterioDeEvaluacion.objects.filter(
            resultado_de_aprendizaje=ra
        )
        resultado+="<h4>Criterios para {0}) {1}</h4>".format(ra.numero, ra.texto)
        for ce in crit_evaluacion:
            #resultado+=control.format(ce.letra+") "+ce.texto)
            resultado+=control.format(ce.texto)
        
        
    return resultado


def get_resultados_aprendizaje_modulo_tabla(modulo_pasado):
    resultado="<h3>Resultados de aprendizaje para {0}(tabla)</h3>".format(modulo_pasado.nombre)
    resultados_aprendizaje=ResultadoDeAprendizaje.objects.filter(modulo=modulo_pasado)
    contador=1
    resultado+="<table border='1'>"
    for r in resultados_aprendizaje:
        resultado+="<tr>"
        resultado+="<td>R.A. "+str(contador)+"</td>"
        resultado+="<td>"+r.texto+"</td>"
        resultado+="</tr>"
        contador+=1
    resultado+="</table>"
    return resultado

def cortar_elementos ( peticion ):
    ciclo=Ciclo.objects.all().order_by("nombre");
    resultado=""
    for c in ciclo:
        
        cursos=Curso.objects.filter(ciclo=c).order_by("num_curso")
        for cu in cursos:
            modulos=Modulo.objects.filter(curso=cu).order_by("nombre")
            for modulo in modulos:
                resultado+=get_datos_modulo(modulo)
        
    return HttpResponse(content=resultado)
        
def index(peticion):
    ciclos_validos=Q(curso__ciclo__abreviatura="DAM")
    ciclos_validos=ciclos_validos | Q(curso__ciclo__abreviatura="ASIR")
    ciclos_validos=ciclos_validos | Q(curso__ciclo__abreviatura="DAW")
    ciclos_validos=ciclos_validos | Q(curso__ciclo__abreviatura="SMIR")
    ciclos_validos=ciclos_validos | Q(curso__ciclo__abreviatura="FPB") 
    modulos = Modulo.objects.filter( ciclos_validos ).order_by("nombre")
    contexto={"modulos":modulos}
    return render_to_response("gestionbd/index.html", contexto)
        
def ver_modulo(peticion, id_pasado):
    modulo=Modulo.objects.get(id=id_pasado)
    resul=get_datos_modulo(modulo)
    contexto={
        "contenido":resul
    }
    return render_to_response("gestionbd/ver_modulo.html", contexto)