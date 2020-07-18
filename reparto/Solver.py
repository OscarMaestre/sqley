#!/usr/bin/env python3
#coding=utf-8

from Configurador import Configurador
configurador=Configurador("..")
configurador.activar_configuracion("ciclos.settings")
import copy, sys

from django.db.models import Q
from gestionbd.models import Profesor, Modulo, EspecialidadProfesor, Grupo
from reparto.models import ModuloEnReparto
import itertools



            
class ProfesorEnReparto(object):
    def __init__(self, profesor):
        self.horas_asignadas    =   0
        self.horas_minimas      =   profesor.horas_minimas
        self.nombre             =   profesor.nombre
        
        self.modulos_asignados  =   []
        self.preferencias       =   None
        
    def set_preferencias(self, preferencias):
        self.preferencias=preferencias
        
    def elegir_modulo(self, lista_modulos_disponibles):
        if self.preferencias==[]:
            return None
        for preferencia in self.preferencias:
            nombre_preferido=preferencia.nombre
            for disponible in lista_modulos_disponibles:
                if disponible.nombre==nombre_preferido:
                    return disponible
            #Fin del for
        #Fin del for
        #Si llegamos aquí no hay ningún modulo preferido
        return None
        
    def constructor_copia(self, profesor_en_reparto):
        self.horas_asignadas        =   profesor_en_reparto.horas_asignadas
        self.horas_minimas          =   profesor_en_reparto.horas_minimas
        self.nombre                 =   profesor_en_reparto.nombre
        self.modulos_asignados      =   []
        for m in profesor_en_reparto.modulos_asignados:
            self.modulos_asignados.append(m)
        
            
    def asignar_modulo(self, modulo):
        if self.llena_horario():
            return False
        #print("Asignando a "+ self.nombre +" el modulo "+modulo.modulo_asociado.nombre)
        self.modulos_asignados.append ( modulo )
        self.horas_asignadas += modulo.modulo_asociado.horas_semanales
        #print("Ahora tiene (en horas):"+str(self.horas_asignadas))
        #print("Su lista de modulos es:")
        for m in self.modulos_asignados:
            #print("\t"+m.modulo_asociado.nombre)
            pass
        return True
        
    def quitar_modulo(self, modulo):
        for m in modulos.asignados:
            if m==modulo:
                self.modulos_asignados.remove ( modulo )
                self.horas_asignadas -= modulo.horas_semanales
        
    def llena_horario(self):
        if self.horas_asignadas==0:
            #print(self.nombre+" aun no llena")
            return False
        if self.horas_asignadas>=self.horas_minimas:
            #print(self.nombre+" ya llena")
            return True
        #print(self.nombre+" aun no llena")
        return False
    
    def __str__(self):
        cad="{0} horas_asignadas:{1}, horas_minimas:{2}".format(
            self.nombre, self.horas_asignadas, self.horas_minimas
        )
        return cad
        
    def get_cadena_situacion(self):
        cad="{0} horas_asignadas:{1}, horas_minimas:{2}\n".format(
            self.nombre, self.horas_asignadas, self.horas_minimas
        )
        for m in self.modulos_asignados:
            cad+="\t {0} ({1}h) {2}\n".format(m.modulo_asociado.nombre,
                                          m.modulo_asociado.horas_semanales,
                                          m.grupo_asociado.nombre_grupo)
        return cad
    
class GestorProfesores(object):
    def __init__(self):
        self.lista_profesores=[]
        self.siguiente_prof=0
        
        
    def constructor_copia(self, gestor):
        
        #print("Haciendo copia:"+gestor.__str__())
        self.lista_profesores=[]
        self.siguiente_prof=gestor.siguiente_prof
        for p in gestor.lista_profesores:
            prof_copia=ProfesorEnReparto(p)
            prof_copia.constructor_copia(p)
            self.lista_profesores.append(prof_copia)
        self.cantidad_profesores=len(self.lista_profesores)
        #mi_cad=self.__str__()
        #print(mi_cad)
        
    def anadir_profesores(self, lista_modelos_profesor):
        print("Lista modelos")
        print(lista_modelos_profesor)
        for modelo in lista_modelos_profesor:
            prof=ProfesorEnReparto(modelo)
            self.lista_profesores.append ( prof )
        self.cantidad_profesores=len(self.lista_profesores)
        
    
    def siguiente_profesor(self):
        profesor_a_devolver=self.lista_profesores[self.siguiente_prof]
        self.siguiente_prof=(self.siguiente_prof+1) % self.cantidad_profesores
        return profesor_a_devolver
    
    def asignar_modulo_a_profesor(self, profesor, modulo):
        nombre_a_buscar=profesor.nombre
        for profesor in self.lista_profesores:
            if profesor.nombre==nombre_a_buscar:
                if profesor.asignar_modulo(modulo):
                    #print ("Horas asignadas:"+str(profesor.horas_asignadas))
                    return True
                return False
        print ("Error, no se encontro un profesor llamado:"+nombre_a_buscar)
        
    def todos_llenan_horario(self):
        for p in self.lista_profesores:
            if not p.llena_horario():
                #print("False en llena horario")
                return False
        print("Una solución hallada:")
        return True
    
    def __str__(self):
        cad=""
        for p in self.lista_profesores:
            cad+=p.get_cadena_situacion()+"\n"
        return cad
    
class Solver(object):
    def __init__(self):
        self.modulos=self.get_modulos()
        self.profesores=self.get_profesores()
        cantidad_modulos=len(self.modulos)
        combinaciones=itertools.combinations(self.modulos, cantidad_modulos-1)
        combinaciones=itertools.permutations(self.modulos)
        self.archivo_soluciones=open("resultados.txt", "w")
        self.num_soluciones=0
        
    def backtracking(self, gestor_profesores, lista_modulos, num_sol=0):
        #print("Nivel:"+str(num_sol))
        if lista_modulos==[]:
            return
        
        gestor_nuevo=GestorProfesores()
        gestor_nuevo.constructor_copia(gestor_profesores)
        
        #print(lista_modulos)
        #print("Nivel de recursividad:"+str(num_sol))
        while not gestor_nuevo.todos_llenan_horario():
            if len(lista_modulos)==0:
                return 
            #print("Iterando..."+str(len(lista_modulos)))
            profesor=gestor_nuevo.siguiente_profesor()
            #print(lista_modulos)
            for modulo in lista_modulos:
                #print("Sigo")
                if gestor_nuevo.asignar_modulo_a_profesor(profesor, modulo):
                    msg="Asignamos {0} a {1}".format(modulo.modulo_asociado.nombre,
                                                     profesor.nombre)
                    print(msg)
                    lista_modulos.remove(modulo)
                    if len(lista_modulos)==0:
                        return 
                    copia=copy.copy(lista_modulos)
                    num_etapa=num_sol+1
                    self.backtracking(gestor_nuevo, copia, num_sol=num_etapa)
        #Fin del while
        print (gestor_nuevo)
            # print("Escrita una posible solucion:"+str(self.num_soluciones))
            # self.num_soluciones+=1
            # 
            # self.archivo_soluciones.write("\n\nComienzo de la solución "+str(self.num_soluciones)+"\n")
            # self.archivo_soluciones.write("##############################\n")
            # 
            # self.archivo_soluciones.write(str(gestor_nuevo))
            # self.archivo_soluciones.write("\nFin de la solución"+str(self.num_soluciones))
            # self.archivo_soluciones.write("\n\n##############################\n")
        print ("Fin de la solucion\n\n\n")
        
    def get_modulos(self):
        lista=ModuloEnReparto.get_modulos()
        return lista
    
    def modulos_tarde(self, lista_modulos):
        modulos_tarde=[]
        for m in lista_modulos:
            if m.es_de_tarde():
                modulos_tarde.append(m)
        return modulos_tarde
    
    #def backtracking2(self, lista_modulos, lista_profesores, num_profesor=0):
        
    
    def get_profesores(self):
        esp_ps=EspecialidadProfesor.objects.filter(especialidad="PS")
        print(esp_ps)
        profesores=Profesor.objects.filter(especialidad=esp_ps).order_by("num_posicion")
        print("Recuperados profesores:")
        print(profesores)
        return profesores
        
if __name__ == '__main__':
    solver=Solver()
    print (solver.modulos)
    print(solver.profesores)
    profesores=solver.profesores
    gestor=GestorProfesores()
    gestor.anadir_profesores(profesores)
    solver.backtracking(gestor, solver.modulos)
    