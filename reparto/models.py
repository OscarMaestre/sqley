from django.db import models
from django.forms import ModelForm
from gestionbd.models import Profesor, Modulo, Grupo
from django.db.models import Q
# Create your models here.



class Reparto ( models.Model ):
    nombre=models.CharField(max_length=30, primary_key=True)
    
class RepartoForm ( ModelForm ):
    class Meta:
        model=Reparto
        fields=["nombre"]

class ModuloEnReparto(models.Model):
    modulo_asociado =   models.ForeignKey(Modulo)
    grupo_asociado  =   models.ForeignKey(Grupo)
        
    def es_de_tarde(self):
        if self.grupo_asociado.nombre_grupo.find("arde")!=-1:
            return True
        return False
    
    def __str__(self):
        cad=self.modulo_asociado.nombre +" ({0}h) ".format(
            self.modulo_asociado.horas_semanales) + self.grupo_asociado.nombre_grupo 
        return cad
    
    @staticmethod
    def get_modulos(con_ordenacion=False):
        
        filtro_modulos_ps=Q(especialidad="PS")
        filtro_modulos_todos=Q(especialidad="TODOS")
        filtro_horas=Q(horas_semanales__gt=0)
        filter_general=filtro_horas & (filtro_modulos_ps | filtro_modulos_todos )
        lista_modulos=[]
        grupos=Grupo.objects.all()
        for g in grupos:
            curso_asociado=g.curso
            #print(curso_asociado)
            if con_ordenacion:
                modulos_asociados=Modulo.objects.filter(
                    curso=curso_asociado).filter(
                    filter_general).order_by("-horas_semanales", "nombre")
            else:
                modulos_asociados=Modulo.objects.filter(curso=curso_asociado).filter(filter_general)
            #print(modulos_asociados)
            for m in modulos_asociados:
                modulo_para_repartir=ModuloEnReparto(modulo_asociado=m,
                                                     grupo_asociado=g)
                
                lista_modulos.append(modulo_para_repartir)
        return lista_modulos
    
    @staticmethod
    def generar_modulos_en_reparto():
        modulos=ModuloEnReparto.get_modulos()
        for m in modulos:
            m.save()
    
    
class Asignacion (models.Model):
    reparto     =   models.ForeignKey(Reparto,              on_delete=models.CASCADE)
    profesor    =   models.ForeignKey(Profesor,             on_delete=models.CASCADE)
    modulo      =   models.ForeignKey(ModuloEnReparto,      on_delete=models.CASCADE)

class PreferenciaProfesor (models.Model):
    profesor    =   models.ForeignKey(Profesor,             on_delete=models.CASCADE)
    modulo      =   models.ForeignKey(ModuloEnReparto,      on_delete=models.CASCADE)
    prioridad   =   models.IntegerField()
    class Meta:
        ordering    =   ["modulo"]