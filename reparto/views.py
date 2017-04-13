from django.shortcuts import render, get_object_or_404
from .models import RepartoForm, Reparto
from django.http import HttpResponseRedirect
from django.db import connection, transaction
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


def index(peticion):
    return render(None, "reparto/index.html")

def repartir(peticion, num_reparto, codigo_profesor, codigo_asignatura):
    return None
