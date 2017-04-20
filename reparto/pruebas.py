#!/usr/bin/env python3

import unittest, copy

from Solver import Solver, GestorProfesores

class TestGestor(unittest.TestCase):
    def test_copia(self):
        solver=Solver()
        profesores=solver.profesores
        gestor=GestorProfesores()
        gestor.anadir_profesores(profesores)
        otro_gestor=copy.deepcopy(gestor)
        
        gestor.siguiente_profesor()
        gestor.siguiente_profesor()
        otro_mas=copy.deepcopy(gestor)
        self.assertEqual(gestor.siguiente_prof, otro_mas.siguiente_prof)
        
if __name__ == '__main__':
    unittest.main()