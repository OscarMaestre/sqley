from django.shortcuts import render, redirect
from django.forms import ModelForm, TextInput, SelectDateWidget, DateField, modelformset_factory, inlineformset_factory
from django.urls import reverse

from .models import Alumno, Modulo, Matricula
from django.db import models

# Create your views here.


class AlumnoForm (ModelForm):
    fecha_nacimiento = DateField(widget=SelectDateWidget(years=range(1950, 2017)))
    class Meta:
        model = Alumno
        exclude =['foto']

class MatriculaForm(ModelForm):
    class Meta:
        model = Matricula
        exclude =['modulo']

def generar_formulario_datos_nuevo_alumno(peticion):
    cp_por_defecto = models.IntegerField(default=13001)
    nuevo_alumno = AlumnoForm()
    nuevo_alumno.cp_notas = cp_por_defecto
    contexto=dict()
    contexto["form_alumno"] = nuevo_alumno    
    return render(peticion, "tutoria/anadir_alumno.html", contexto)


def procesar_alumno_entrante(peticion):
    alumno_introducido = AlumnoForm(peticion.POST)
    if alumno_introducido.is_valid():
        alumno_introducido.save()
        dni=peticion.POST["dni"]
        return redirect('tutoria:editar', dni)
    else:
        alumno_introducido = AlumnoForm(peticion.POST)
        contexto=dict()
        contexto["form_alumno"] = alumno_introducido
        return render(peticion, "tutoria/anadir_alumno.html", contexto)
        
def anadir(peticion):
    if peticion.method=="POST":
        redireccion=procesar_alumno_entrante(peticion)
        return redireccion
    else:
        vista=generar_formulario_datos_nuevo_alumno(peticion)
        return vista
    
    
def editar(peticion, id):
    contexto=dict()
    if peticion.method=="POST":
        alumno_a_modificar=Alumno.objects.get(dni=id)
        alumno_a_modificar.dni=peticion.POST["dni"]
        alumno_introducido = AlumnoForm(peticion.POST, instance=alumno_a_modificar)
        alumno_introducido.save()
        contexto["form_alumno"] = alumno_introducido
        contexto["dni"]=id
        contexto["mensaje"]="Tus cambios se han guardado."
        return render(peticion, "tutoria/editar_alumno.html", contexto)
    
    else:
        alumno_a_editar=Alumno.objects.get(dni=id)
        alumno_introducido = AlumnoForm(instance=alumno_a_editar)
    
        contexto["form_alumno"] = alumno_introducido
        contexto["dni"]=id
        return render(peticion, "tutoria/editar_alumno.html", contexto)
    
    
def index_matricula(peticion):
    modulos=Modulo.objects.all()
    contexto=dict()
    contexto["modulos"]=modulos
    print (modulos[0].curso.nombre_curso)
    return render(peticion, "tutoria/index_matriculas.html", contexto)


def realizar_matricula(peticion, modulo):
    if peticion.method=="POST":
        pass
    else:
        
        todos_alumnos=Alumno.objects.all()
        lista_ids=[]
        for a in todos_alumnos:
            lista_ids.append({'alumno':a.dni,})
        print(lista_ids)
        ClaseFabricaModelosMatricula= modelformset_factory(Matricula, MatriculaForm,extra=len(lista_ids))
        #fabrica_modelos_matricula=ClaseFabricaModelosMatricula(initial=lista_ids )
        fabrica_modelos_matricula=ClaseFabricaModelosMatricula(initial=lista_ids)
        contexto=dict()
        contexto["conjunto_matriculas"]=fabrica_modelos_matricula
        contexto["id_modulo"]=modulo
        print(fabrica_modelos_matricula)
        return render(peticion, "tutoria/realizar_matricula.html", contexto)