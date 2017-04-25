from django.shortcuts import render, get_object_or_404
from .models import RepartoForm, Reparto, Asignacion, PreferenciaProfesor, ModuloEnReparto
from gestionbd.models import Profesor
from django.http import HttpResponseRedirect
from django.db import connection, transaction
from django.forms import formset_factory, ModelForm
from django.core.urlresolvers import reverse

EXTRACCION_MODULOS="""
SELECT mod.id, mod.nombre, mod.horas_semanales,
        g.nombre_grupo, ciclos.nivel_profesional, mod.especialidad
    from ciclos, modulos as mod, grupos as g, cursos as cur
        where
            mod.curso_id=cur.id
        and
            especialidad<>'PT'
        and
            g.curso_id=cur.id
        and
            cur.ciclo_id=ciclos.id
        
    order by horas_semanales desc, num_curso desc, nivel_profesional desc;
"""
# Create your views here.

class AsignacionForm(ModelForm):
    class Meta:
        model = PreferenciaProfesor
        fields=["modulo", "prioridad"]

def index(peticion):
    return render(None, "reparto/index.html")

def repartir(peticion, num_reparto, codigo_profesor, codigo_asignatura):
    return None



def asignar_preferencias(peticion):
    profesores=Profesor.objects.all().order_by("num_posicion")
    
    contexto=dict()
    contexto["profesores"]=profesores
    return render(peticion, "reparto/asignar_preferencias.html", contexto)

def almacenar_preferencias(peticion, id_profesor=None):
    if peticion.method=='POST':
        print(peticion)
        
        asignaciones_formset=formset_factory(AsignacionForm)
        formularios=asignaciones_formset(peticion.POST)
        if formularios.is_valid():
            print("Todo perfecto")
            return render(None, "reparto/index.html")
        else:
            print("Error de validacion")
            return render(None, "reparto/index.html")
    modulos_en_reparto=ModuloEnReparto.objects.all().order_by("modulo_asociado__nombre")
    profesor=Profesor.objects.get(id=id_profesor)
    #cantidad_modulos_a_repartir=len(modulos_en_reparto)
    cantidad_modulos_a_repartir=14
    contexto=dict()
    
    asignaciones_formset=formset_factory(AsignacionForm,
                extra=cantidad_modulos_a_repartir)   
    contexto["nombre_profesor"]=Profesor.objects.get(id=id_profesor)
    contexto["formularios"]=asignaciones_formset
    contexto["id_profesor"]=id_profesor
    return render(peticion, "reparto/almacenar_preferencias.html", contexto)
