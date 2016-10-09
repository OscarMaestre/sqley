from django.shortcuts import render
from django.forms import ModelForm, ModelMultipleChoiceField
from .models import *
from gestionbd.models import *
# Create your views here.


class ProgramacionForm ( ModelForm):
    class Meta:
        model = Programacion
        fields = ["nombre", "modulo", "profesor"]
        
class ProgramacionObjetivosForm ( ModelForm):
    def __init__(self, ciclo_pasado, *args, **kwargs):
        super(ProgramacionObjetivosForm, self).__init__(*args, **kwargs)
        self.fields['objetivos'] = ModelMultipleChoiceField(
            queryset=ObjetivoGeneral.objects.filter(ciclo=ciclo_pasado)
        )
    class Meta:
        model = Programacion
        fields = ["objetivos"]

def index ( peticion ):
    progs=Programacion.objects.all()
    print(progs)
    contexto={"titulo":"Indice de opciones",
        "programaciones":progs
    }
    return render (peticion, "programaciones/index.html", contexto )

def crear(peticion):
    pass

def editar(peticion, id):
    programacion_a_editar=Programacion.objects.get(pk=id)
    if peticion.method=="POST":
        form = ProgramacionForm ( peticion.POST, instance= programacion_a_editar )
        if form.is_valid():
            form.save()
            return index(peticion)
    else:
        
        nombre_programacion=programacion_a_editar.nombre
        
        formulario_programacion=ProgramacionForm(instance=programacion_a_editar)
        contexto={
            "id_programacion":id,
            "nombre_programacion":nombre_programacion,
            "formulario":formulario_programacion.as_table(),
            "modulos":programacion_a_editar.modulo.all()
        }
        return render (peticion, "programaciones/editar.html", contexto )
    
def editar_objetivos_generales ( peticion, id_programacion, id_modulo ):
    modulo=Modulo.objects.get(pk=id_modulo)
    ciclo=modulo.curso.ciclo
    programacion_a_editar=Programacion.objects.get(pk=id_programacion)
    if peticion.method=="POST":
        objetivos_para_establecer=peticion.POST["objetivos"]
        programacion_a_editar.objetivos.clear()
        programacion_a_editar.objetivos.add(objetivos_para_establecer)
        return index(peticion)
    else:
        
        nombre_programacion=programacion_a_editar.nombre
        
        formulario_programacion=ProgramacionObjetivosForm(
            ciclo_pasado=ciclo, instance=programacion_a_editar)
        contexto={
            "id_programacion":id_programacion,
            "id_modulo":id_modulo,
            "nombre_programacion":nombre_programacion,
            "formulario":formulario_programacion.as_table()
        }
        return render (peticion,
                       "programaciones/editar_objetivos_generales.html",
                       contexto )