from django.shortcuts import render
from django.forms import ModelForm, TextInput, SelectDateWidget, DateField
from .models import Alumno
from django.db import models

# Create your views here.


class AlumnoForm (ModelForm):
    fecha_nacimiento = DateField(widget=SelectDateWidget)
    class Meta:
        model = Alumno
        exclude =['foto']

def anadir(peticion):
    
    cp_por_defecto = models.IntegerField(default=13001)
    nuevo_alumno = AlumnoForm()
    nuevo_alumno.cp_notas = cp_por_defecto
    contexto=dict()
    
    contexto["form_alumno"] = nuevo_alumno
    
    return render(peticion, "tutoria/anadir_alumno.html", contexto)