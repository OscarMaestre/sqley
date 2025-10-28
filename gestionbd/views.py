from django.shortcuts import render, get_object_or_404, redirect

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import *
# Create your views here.
from .forms import ResultadoAprendizajeFormset
     
def index(peticion):
    ciclos_validos=Q(curso__ciclo__abreviatura="DAM")
    ciclos_validos=ciclos_validos | Q(curso__ciclo__abreviatura="ASIR")
    ciclos_validos=ciclos_validos | Q(curso__ciclo__abreviatura="DAW")
    ciclos_validos=ciclos_validos | Q(curso__ciclo__abreviatura="SMIR")
    ciclos_validos=ciclos_validos | Q(curso__ciclo__abreviatura="FPB") 
    modulos = Modulo.objects.filter( ciclos_validos ).order_by("nombre")
    contexto={"modulos":modulos}
    return render(peticion, "gestionbd/index.html", contexto)
        
def ver_modulo(peticion, id):
    modulo=Modulo.objects.get(id=id)
    contexto={
        "modulo":modulo
    }
    return render(peticion, "gestionbd/ver_modulo.html", contexto)

def editar_criterios_aprendizaje(peticion, idmodulo):
    modulo = get_object_or_404(Modulo, id=idmodulo)


    formset = ResultadoAprendizajeFormset(peticion.POST or None, instance=modulo)

    if peticion.method == 'POST' and formset.is_valid():
        formset.save()
        messages.success(peticion, "Cambios a los criterios guardados correctamente")
        return redirect('gestionbd:ver', id=modulo.id)
    else:
        for form in formset:   
            if form.errors:
                print(form.errors)
        print(formset.non_form_errors())
    return render(peticion, 'gestionbd/editar_criterios.html', {
        'modulo': modulo,
        'formset': formset,
    })