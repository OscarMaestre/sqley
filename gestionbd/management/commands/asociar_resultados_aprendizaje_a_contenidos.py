from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from gestionbd.models import Modulo,ResultadoDeAprendizaje,Contenido, ResultadoContenido

class Command(BaseCommand):
    help = "Asocia determinados resultados de aprendizaje a ciertos contenidos para poder generar correctamente tablas de programaciones en los ficheros corta_y_pega.html"

    
    def se_pueden_asociar_resultados_a_contenidos(self, modulo):
        resultados=ResultadoDeAprendizaje.objects.filter(modulo=modulo).order_by("numero")
        #Cogemos sus contenidos
        contenidos=Contenido.objects.filter(modulo=modulo).order_by("numero")
        cantidad_resultados=len(resultados)
        cantidad_contenidos=len(contenidos)
        # print(f"Asociando {cantidad_contenidos} contenidos con {cantidad_resultados} resultados")
        if cantidad_resultados!=cantidad_contenidos:
            self.imprimir_error(modulo.curso.ciclo, modulo, f"No hay la misma cantidad de contenidos ({cantidad_contenidos}) que de resultados ({cantidad_resultados})")
            return (False, None, None )
        return (True, contenidos, resultados)
    
    def imprimir_error (self, ciclo, modulo, mensaje):
        print("\n=====================\nError en ciclo:" + str(ciclo))
        print("\tError en modulo:" + str(modulo))
        print("\t\t"+mensaje)
        print("=====================\n")
        
    def _asociar(self, contenido, resultado, modulo):
        asociacion=ResultadoContenido.objects.filter(resultado=resultado, contenido=contenido)
        if len(asociacion)==0:
            
            asociacion=ResultadoContenido(contenido=contenido, resultado=resultado, modulo=modulo)
            asociacion.save()
            #print("Creada asociacion:"+str(contenido)+"<->"+str(resultado))
        else:
            self.imprimir_error(contenido.modulo.curso.ciclo, contenido.modulo, f"Ya existia la asociacion {contenido}<->{resultado}")
    #Este método toma un módulo y asocia el RA 1 con el contenido 1,
    #el RA2 con el contenido 2 y así sucesivamente
    def asociar_resultados_con_contenidos(self,modulo):
        (se_puede_hacer_la_asociacion, contenidos, resultados)=self.se_pueden_asociar_resultados_a_contenidos(modulo)
        
        if not se_puede_hacer_la_asociacion:
            return
        for pos, contenido in enumerate(contenidos):
            self._asociar(contenidos[pos], resultados[pos], modulo)

    def handle(self, *args, **options):
        
        with transaction.atomic():
            modulos=Modulo.objects.all()
            for modulo in modulos:    
                #Cogemos sus resultados de aprendizaje
                self.asociar_resultados_con_contenidos(modulo)
        

