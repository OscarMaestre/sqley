#!/usr/bin/env python3

import unittest, copy

from Solver import Solver, GestorProfesores

class TestGestor(unittest.TestCase):
    def test_copia(self):
        solver=Solver()
        profesores=solver.profesores
        modulos=solver.modulos
        prof_1=profesores[0]
        gestor=GestorProfesores()
        gestor.anadir_profesores(profesores)
        gestor.asignar_modulo_a_profesor(prof_1, modulos[0])
        otro_gestor=copy.deepcopy(gestor)
        lista_profesores=otro_gestor.lista_profesores
        prof_is=lista_profesores[0]
        print(prof_is)
        gestor.siguiente_profesor()
        gestor.siguiente_profesor()
        otro_mas=copy.deepcopy(gestor)
        self.assertEqual(gestor.siguiente_prof, otro_mas.siguiente_prof)
        
if __name__ == '__main__':
    unittest.main()