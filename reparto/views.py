from django.shortcuts import render
from .models import RepartoForm
from django.http import HttpResponseRedirect
from django.db import connection
from django.core.urlresolvers import reverse

EXTRACCION_MODULOS="""
SELECT mod.id, mod.nombre, mod.horas_semanales, g.nombre_grupo, ciclos.nivel_profesional
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


def index(peticion):
    return render(None, "reparto/index.html")

def repartir(peticion, num_reparto, codigo_profesor, codigo_asignatura):
    return None



def crear_asignaturas_reparto ( id_reparto ):
    print ("Creando para "+ str(id_reparto))
    
def crear(peticion):
    if peticion.method=="POST":
        formulario_pasado=RepartoForm ( peticion.POST )
        if formulario_pasado.is_valid():
            formulario_pasado.save()
            id_reparto=formulario_pasado.instance.id
            ##print ( dir(formulario_pasado.instance))
            crear_asignaturas_reparto ( formulario_pasado.instance.id )
            return HttpResponseRedirect ( reverse("reparto:elegir {0}".format(id_reparto)) )
        else:
            print ("Meec")
    else:
        formulario=RepartoForm()
        datos={
            "formulario":formulario.as_table()
        }
        
        return render(peticion, "reparto/crear_reparto.html", datos)
    
def elegir ( peticion, num_reparto=None, num_profesor=None, num_asignatura=None ):
    datos={
        "num_reparto":num_reparto,
        "num_profesor":num_profesor,
        "num_asignatura":num_asignatura
    }
    return render ( peticion, "reparto/elegir.html", datos)
    