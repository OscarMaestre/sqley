from django.contrib import admin
from django import forms
from .models import *
from gestionbd.models import *



# Register your models here.
admin.site.register ( UnidadDeTrabajo )
admin.site.register ( PuntoMetodologico )
admin.site.register ( Evaluacion )
admin.site.register ( RecursoDidactico )
admin.site.register ( Programacion )
admin.site.register ( ObjetivosModulo)
admin.site.register ( CompetenciasModulo)
admin.site.register ( InstrumentoEvaluacion )
admin.site.register ( Interviene )