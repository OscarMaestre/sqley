from django.shortcuts import render, get_object_or_404, redirect

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import *
# Create your views here.
from .forms import ResultadoAprendizajeFormset, CriterioDeEvaluacionFormset     
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

def dualizar_criterios_individuales(peticion, idra):
    ra = get_object_or_404(ResultadoDeAprendizaje, id=idra)


    formset = CriterioDeEvaluacionFormset(peticion.POST or None, instance=ra)

    if peticion.method == 'POST' and formset.is_valid():
        formset.save()
        modulo=ra.modulo
        messages.success(peticion, "Cambios a los criterios guardados correctamente")
        return redirect('gestionbd:mostrar_ras_dualizar', idmodulo=modulo.id)
    else:
        errores=[]
        for form in formset:   
            if form.errors:
                print(form.errors)
                errores.append(form.errors)
        txt_errores="<p>".join(errores)
        messages.error(peticion, txt_errores)
    return render(peticion, 'gestionbd/dualizar_criterios_individuales.html', {
        'formset': formset,
    })


def mostrar_ras_dualizar(peticion, idmodulo):
    modulo = get_object_or_404(Modulo, id=idmodulo)
    return render(peticion, 'gestionbd/mostrar_resultados_y_criterios_modulo.html', {'modulo':modulo})


def enviar_criterios_a_empresa(criterios, valor_booleano, peticion, prefijo):
    for criterio in criterios:
        criterio.va_a_empresa=valor_booleano
        messages.success(peticion, prefijo+criterio.texto)
        criterio.save()
    return

def activar_dualizacion_todo_ra(peticion, idra):
    ra = get_object_or_404(ResultadoDeAprendizaje, id=idra)
    criterios=ra.criteriodeevaluacion_set.all()
    modulo=ra.modulo
    enviar_criterios_a_empresa(criterios, True, peticion, "Dualizado:")
    return redirect('gestionbd:mostrar_ras_dualizar', idmodulo=modulo.id)
    
def desactivar_dualizacion_todo_ra(peticion, idra):
    ra = get_object_or_404(ResultadoDeAprendizaje, id=idra)
    criterios=ra.criteriodeevaluacion_set.all()
    modulo=ra.modulo
    enviar_criterios_a_empresa(criterios, False, peticion, "Desdualizado")
    return redirect('gestionbd:mostrar_ras_dualizar', idmodulo=modulo.id)
    
