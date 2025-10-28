from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import CriterioDeEvaluacion, ResultadoDeAprendizaje, Modulo

ResultadoAprendizajeFormset = inlineformset_factory(
    Modulo, ResultadoDeAprendizaje,
    fields=('texto', 'porcentaje_empresa', 'porcentaje_centro'),
    extra=0,
)
