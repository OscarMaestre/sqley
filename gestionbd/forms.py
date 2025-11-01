from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import CriterioDeEvaluacion, ResultadoDeAprendizaje, Modulo

ResultadoAprendizajeFormset = inlineformset_factory(
    Modulo, ResultadoDeAprendizaje,
    fields=('texto',),
    extra=0,
)
CriterioDeEvaluacionFormset=inlineformset_factory(
    ResultadoDeAprendizaje,CriterioDeEvaluacion,
    fields=['texto', 'va_a_empresa'],
    extra=0
)