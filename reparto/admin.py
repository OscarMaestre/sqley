from django.contrib import admin
from .models import *
from programaciones.models import *
# Register your models here.

admin.site.register ( Reparto )
admin.site.register ( Profesor )
admin.site.register ( ModuloPorAsignar )
admin.site.register ( ModuloAsignado )
admin.site.register ( UnidadDeTrabajo )
admin.site.register ( PuntoMetodologico )
admin.site.register ( Evaluacion )
admin.site.register ( RecursoDidactico )
admin.site.register ( Programacion )
admin.site.register ( ProcedimientoEvaluacion )
admin.site.register ( MecanismoEvaluacion )
admin.site.register ( Interviene )