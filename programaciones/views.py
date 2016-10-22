from django.shortcuts import render, redirect
from django.forms import ModelForm, ModelMultipleChoiceField
from .models import *
from gestionbd.models import *
from django.contrib import admin

# Create your views here.


class ProgramacionForm ( ModelForm ):
    class Meta:
        model = Programacion
        fields = ["nombre",  "profesor"]


class UT_RA_Form ( ModelForm ):
    def __init__(self,*args,**kwargs):
        super (UT_RA_Form,self ).__init__(*args,**kwargs) # populates the post
        
    def establecer_filtrado(self, programacion_pasada):
        print("Programacion pasada:"+str(programacion_pasada))
        if programacion_pasada!=None:
            resultados_aprendizaje_asociados=ResultadoDeAprendizaje.objects.filter(
                modulo=programacion_pasada.modulo.all()
            )
            
            #programacion_asociada=Programacion.objects.filter(nombre=programacion.nombre)
            self.fields["resultado_aprendizaje"].queryset=resultados_aprendizaje_asociados
            
            #self.fields["programacion"].queryset=programacion_asociada
        
    class Meta:
        model=UnidadDeTrabajo
        fields=["numero", "nombre", "sesiones", "evaluaciones", 
                "resultado_aprendizaje",
                "programacion"]
        
    
class UT_Criterios_Form ( ModelForm ):
    def __init__(self,*args,**kwargs):
        super (UT_Criterios_Form,self ).__init__(*args,**kwargs) # populates the post
        
    def establecer_filtrado(self, unidad_tecnica):
        print(unidad_tecnica.resultado_aprendizaje)
        resultados_aprendizaje_asociados=unidad_tecnica.resultado_aprendizaje.all()
        print(resultados_aprendizaje_asociados)
        
        criterios_asociados=CriterioDeEvaluacion.objects.filter(
            resultado_de_aprendizaje=resultados_aprendizaje_asociados
        )
        #programacion_asociada=Programacion.objects.filter(nombre=programacion.nombre)
        self.fields["resultado_aprendizaje"].queryset=resultados_aprendizaje_asociados
        self.fields["criterios"].queryset=criterios_asociados
        #self.fields["programacion"].queryset=programacion_asociada
        
    class Meta:
        model=UnidadDeTrabajo
        fields=["numero", "nombre", "sesiones", "evaluaciones", 
                "resultado_aprendizaje", "criterios",
                "programacion"]
        



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
        }
        return render (peticion, "programaciones/editar.html", contexto )
    
def editar_objetivos_generales ( peticion, id_programacion ):
    programacion_a_editar=Programacion.objects.get(pk=id_programacion)
    if peticion.method=="POST":
        objetivos_para_establecer=peticion.POST["objetivos"]
        programacion_a_editar.objetivos.clear()
        programacion_a_editar.objetivos.add(objetivos_para_establecer)
        return index(peticion)
    else:
        
        nombre_programacion=programacion_a_editar.nombre
        
        formulario_programacion=FormObjetivosGeneralesRestringidos(
            initial=[{"programacion":programacion_a_editar, "objetivos":None}])
        contexto={
            "id_programacion":id_programacion,
            "nombre_ciclo":programacion_a_editar.modulo.curso.ciclo.nombre,
            "nombre_programacion":nombre_programacion,
            "formulario":formulario_programacion.as_table()
        }
        return render (peticion,
                       "programaciones/editar_objetivos_generales.html",
                       contexto )
    
    
def crear_ut(peticion=None, id_programacion=None):
    programacion_asociada=Programacion.objects.get(pk=id_programacion)
    contexto={
        "programacion_asociada":programacion_asociada
    }
    if peticion.method=="POST":
        print (peticion.POST)
        form = UT_RA_Form ( peticion.POST )
        if form.is_valid():
            form.save()
            peticion.method=None
            return crear_ut(peticion=peticion,id_programacion=id_programacion)
    else:
        form_ut=UT_RA_Form()
        form_ut.establecer_filtrado(programacion_asociada)
        contexto["formulario"]=form_ut.as_table()
        return render(peticion, "programaciones/crear_ut.html", contexto)
        
    
def asignar_criterios(peticion, id_unidad_tecnica):
    ut_asociada=UnidadDeTrabajo.objects.get(id=id_unidad_tecnica)
    if peticion.method=="POST":
        form = UT_Criterios_Form ( peticion.POST )
        if form.is_valid():
            print(peticion.POST)
            for c in peticion.POST["criterios"]:
                i=Interviene()
                i.criterio_id=c
                i.unidad_de_trabajo=ut_asociada
                i.es_criterio_minimo=False
                i.ponderacion=15;
                i.calificador=Calificador.objects.all()[0]
                i.save()
            id_prog_asociada=ut_asociada.programacion.id
            peticion.POST=None
            return redirect("programaciones:crear_ut", id_prog_asociada)
    else:
        form_criterios=UT_Criterios_Form(instance=ut_asociada)
        form_criterios.establecer_filtrado(ut_asociada)
        contexto={
            "unidad_asociada":ut_asociada,
            "formulario":form_criterios
        }
        return render(peticion, "programaciones/asignar_criterios.html", contexto)