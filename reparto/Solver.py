#!/usr/bin/env python3


from Configurador import Configurador
configurador=Configurador("..")
configurador.activar_configuracion("ciclos.settings")

from django.db.models import Q
from gestionbd.models import Profesor, Modulo, EspecialidadProfesor
import itertools

class ProfesorEnReparto(object):
    def __init__(self, profesor):
        self.horas_asignadas=0
        self.horas_maximas=profesor.horas_maximas
        
        self.modulos_asignados=[]
        
    def asignar_modulo(self, modulo):
        self.modulos_asignados.append ( modulo )
        self.horas_asignadas += modulo.horas_semanales
        
    def quitar_modulo(self, modulo):
        for m in modulos.asignados:
            if m==modulo:
                self.modulos_asignados.remove ( modulo )
                self.horas_asignadas -= modulo.horas_semanales
        
    def llena_horario(self):
        if self.horas_asignadas>=self.horas_maximas:
            return True
        return False
        
class GestorProfesores(object):
    def __init__(self):
        self.lista_profesores=[]
        self.siguiente_profesor=0
    def anadir_profesor(self, profesor):
        self.lista_profesores.append ( profesor )
        
    def todos_llenan_horarios(self):
        for p in self.lista_profesores:
            if not p.llena_horario:
                return False
        return True
    
    
    
class Solver(object):
    def __init__(self):
        self.modulos=self.get_modulos()
        self.profesores=self.get_profesores()
        cantidad_modulos=len(self.modulos)
        combinaciones=itertools.combinations(self.modulos, cantidad_modulos-1)
        combinaciones=itertools.permutations(self.modulos)
        print(dir(combinaciones))
        
        i=0
        for indice, combinacion in enumerate(combinaciones):
            i=i+1
            if i%10000000==0:
                print (i)
            continue
            print("############     " + str(indice) + "   #####################")
            print (combinacion)
            print("############     " + str(indice) + "   #####################")
        print ("Total:"+str(i))
        
    def get_modulos(self):
        filtro_modulos_ps=Q(especialidad="PS")
        filtro_modulos_todos=Q(especialidad="TODOS")
        filtro_horas=Q(horas_semanales__gt=0)
        filtro_todos=( filtro_modulos_ps  | filtro_modulos_todos  )&  filtro_horas 
        modulos=Modulo.objects.filter(filtro_todos).order_by("-horas_semanales", "nombre")
        return modulos
    
    def get_profesores(self):
        esp_ps=EspecialidadProfesor.objects.filter(especialidad="PS")
        profesores=Profesor.objects.filter(especialidad=esp_ps).order_by("num_posicion")
        return profesores
        
if __name__ == '__main__':
    solver=Solver()
    