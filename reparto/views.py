from django.shortcuts import render
from .models import RepartoForm
from django.http import HttpResponseRedirect
# Create your views here.


def index(peticion):
    return render(None, "reparto/index.html")

def repartir(peticion, num_reparto, codigo_profesor, codigo_asignatura):
    return None

def crear(peticion):
    if peticion.method=="POST":
        formulario_pasado=RepartoForm ( peticion.POST )
        if formulario_pasado.is_valid():
            formulario_pasado.save()
            return HttpResponseRedirect ("reparto/index")
    else:
        formulario=RepartoForm()
        datos={
            "formulario":formulario.as_table()
        }
        
        return render(peticion, "reparto/crear_reparto.html", datos)