#!/usr/bin/env python3


from Configurador import Configurador
configurador=Configurador("..")
configurador.activar_configuracion("ciclos.settings")
import copy

from django.db.models import Q
from gestionbd.models import Profesor, Modulo, EspecialidadProfesor
import itertools

class ProfesorEnReparto(object):
    def __init__(self, profesor):
        self.horas_asignadas    =   0
        self.horas_minimas      =   profesor.horas_minimas
        self.nombre             =   profesor.nombre
        
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
        
        
    def anadir_profesores(self, lista_modelos_profesor):
        for modelo in lista_modelos_profesor:
            prof=ProfesorEnReparto(modelo)
            self.lista_profesores.append ( prof )
        self.cantidad_profesores=len(self.lista_profesores)
        
    
    def siguiente_profesor(self):
        profesor_a_devolver=self.lista_profesores[self.siguiente_profesor]
        self.siguiente_profesor=(self.siguiente_profesor+1) % self.cantidad_profesores
        return profesor_a_devolver
    
    def asignar_modulo_a_profesor(self, profesor, modulo):
        nombre_a_buscar=profesor.nombre
        for profesor in self.lista_profesores:
            if profesor.nombre==nombre_a_buscar:
                profesor.asignar_modulo(modulo)
                return
        print ("Error, no se encontro un profesor llamado:"+nombre_a_buscar)
        
    def todos_llenan_horario(self):
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
        
        
        
    def backtracking(self, lista_profesores, lista_modulos, num_sol=0):
        gestor_nuevo=copy.deepcopy(lista_profesores)
        print(lista_profesores.lista_profesores)
        while not gestor_nuevo.todos_llenan_horario():
            profesor=gestor_nuevo.siguiente_profesor()
            
            for modulo in lista_modulos:
                profesor.asignar_modulo(modulo)
                lista_modulos.remove(modulo)
                print("Pasando a la etapa:"+str(num_sol))
                self.backtracking(lista_profesores, lista_modulos, num_sol+1)
                print("Cerrando la etapa:"+str(num_sol))
        print ("Fin")
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
    profesores=solver.profesores
    gestor=GestorProfesores()
    gestor.anadir_profesores(profesores)
    solver.backtracking(gestor, solver.modulos)
    