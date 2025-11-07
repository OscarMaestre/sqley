from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import CriterioDeEvaluacion, ResultadoDeAprendizaje, Modulo, PuntoDeContenido

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

class PuntoDeContenidoForm(forms.ModelForm):
    class Meta:
        model=PuntoDeContenido
        fields=["texto", "criterio_de_evaluacion"]
    def __init__(self, *args, criterios_qs=None, **kwargs):
        super().__init__(*args, **kwargs)
        if criterios_qs is not None:
            self.fields['criterio_de_evaluacion'].queryset = criterios_qs