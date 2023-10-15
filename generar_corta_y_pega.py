#!/usr/bin/env python3
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("ciclos")
configurador.activar_configuracion ("ciclos.settings")

from gestionbd.models import Modulo, Profesor, Ciclo, Competencia, CompetenciaGeneral, Contenido, ResultadoDeAprendizaje, PuntoDeContenido, ObjetivoGeneral, CriterioDeEvaluacion
from django.db.models.expressions import Q
from django.template.loader import render_to_string
import sys, os


class UnidadDidactica(object):
    def __init__(self) -> None:
        self.puntos_contenido=[]
        self.criterios_evaluacion=[]
    def set_horas_asignadas(self, horas):
        self.horas=horas
    def set_numero(self, numero):
        self.numero=numero
    def set_nombre(self, nombre):
        self.nombre=nombre
    def set_resultado_aprendizaje(self, resultado_aprendizaje):
        self.resultado_aprendizaje=resultado_aprendizaje
    def add_punto_contenido(self, punto_contenido):
        self.puntos_contenido.append(punto_contenido)
    def add_criterio_evaluacion(self, criterio_evaluacion):
        self.criterios_evaluacion.append(criterio_evaluacion)
    def __str__(self) -> str:
        return f">>{self.nombre}-{self.resultado_aprendizaje}"

def generar_lista_unidades_didacticas(modulo):
    contenidos=modulo.contenido_set.all().order_by("numero")
    unidades=[]
    num_unidad=1
    horas_anuales=modulo.horas_anuales
    horas_por_unidad=int(horas_anuales/len(contenidos))
    for c in contenidos:
        u=UnidadDidactica()
        u.set_nombre(c.texto)
        u.set_numero(num_unidad)
        u.set_horas_asignadas(horas_por_unidad)
        num_unidad=num_unidad+1
        num_contenido=c.numero
        print("Num contenido :"+str(num_contenido))
        #Cuidado, no todos los contenidos tienen un resultado de aprendizaje asociado
        try:
            resultado_aprendizaje_asociado=modulo.resultadodeaprendizaje_set.filter(numero=num_contenido)[0]
        except IndexError:
            continue
        u.set_resultado_aprendizaje(resultado_aprendizaje_asociado.texto)
        for criterio in resultado_aprendizaje_asociado.criteriodeevaluacion_set.all():
            u.add_criterio_evaluacion(criterio.texto)
        
        for punto_contenido in c.puntodecontenido_set.all():
            u.add_punto_contenido(punto_contenido.texto)
        unidades.append(u)
    return unidades

DIRECTORIO_RESULTADOS   =   "para_cortar_y_pegar"
def generar_fichero_corta_y_pega ( codigo_modulo_segun_jccm, directorio_fichero_resultado):
    modulos = Modulo.objects.filter ( codigo_junta = codigo_modulo_segun_jccm ) #Importante, solo debe haber un resultado
    
    if len ( modulos ) == 0:
        print ("No hay ningun modulo cuyo campo codigo_junta sea " + codigo_modulo_segun_jccm)
        sys.exit(-1)
    if len(modulos)>1:
        print("Se encontraron varios modulos:"+str(len(modulos)))
        print(codigo_modulo_segun_jccm)
        print(modulos)
        
    for objeto_modulo in modulos:
        
        #Importante, solo debe haber un resultado
        #print (objeto_modulo[0])
        curso_asociado_al_modulo    =   objeto_modulo.curso
        ciclo_asociado              =   curso_asociado_al_modulo.ciclo
        #print (ciclo_asociado)
        
        contenidos_del_modulo       =   objeto_modulo.contenido_set.all()
        competencia_general         =   ciclo_asociado.competenciageneral_set.all()[0]
        print ("Procesando modulo "+objeto_modulo.nombre+" asociado al ciclo "+ ciclo_asociado.abreviatura)
        objetivos_generales_del_ciclo   =   ObjetivoGeneral.objects.filter ( ciclo = ciclo_asociado )
        
        resultados_de_aprendizaje       =   ResultadoDeAprendizaje.objects.filter ( modulo = objeto_modulo )
        
        horas_modulo                    =   int(objeto_modulo.horas_anuales)
        horas_para_perder_ev_continua   =   round(horas_modulo*0.2)
        criterios_de_evaluacion         =   CriterioDeEvaluacion.objects.filter(resultado_de_aprendizaje__modulo=objeto_modulo)
        
        competencias                    =   Competencia.objects.filter(ciclo=ciclo_asociado)
        
        # cualificaciones                 =   ciclo_asociado.ciclotienecualificacion_set.all()
        #Mostramos las completas
        cualificaciones_completas         =   ciclo_asociado.ciclotienecualificacion_set.filter(es_completa=True)
        #Y aquí las incompletas
        cualificaciones_incompletas       =   ciclo_asociado.ciclotienecualificacion_set.filter(es_completa=False)
        #print(cualificaciones)
        #print (criterios_de_evaluacion)
        

        #Aquí se generan algunas posibles unidades didácticas
        unidades_didacticas             =   generar_lista_unidades_didacticas(objeto_modulo)


        #print (objetivos_generales_del_ciclo)
        
        #Se genera el fichero
        
        nombre_fichero=objeto_modulo.nombre.replace(" ", "_")
        nombre_fichero=nombre_fichero.strip(".")
        nombre_fichero=nombre_fichero+"_"+ciclo_asociado.abreviatura+".html"
        #Debido a que el nombre del modulo a veces lleva un punto al final podría haber nombre como "modulo..html"
        #Asi que quitamos el ..
        nombre_fichero = nombre_fichero.replace("..", ".")
        
        
        nombre_fichero = directorio_fichero_resultado + os.sep + nombre_fichero 
        
        diccionario=dict()
        diccionario["objetivos_generales"]          =       objetivos_generales_del_ciclo
        diccionario["nombre_modulo"]                =       objeto_modulo.nombre
        diccionario["resultados_aprendizaje"]       =       resultados_de_aprendizaje
        diccionario["competencias"]                 =       competencias
        diccionario["cualificaciones_completas"]    =       cualificaciones_completas
        diccionario["cualificaciones_incompletas"]  =       cualificaciones_incompletas
        diccionario["ciclo"]                        =       ciclo_asociado
        diccionario["contenidos"]                   =       contenidos_del_modulo
        diccionario["competencia_general"]          =       competencia_general
        diccionario["horas_modulo"]                 =       horas_modulo
        diccionario["horas_perdida_ev_continua"]    =       horas_para_perder_ev_continua
        diccionario["unidades_didacticas"]          =       unidades_didacticas
        contenido_fichero = render_to_string("programaciones/para_cortar_y_pegar.html", diccionario)
        with open(nombre_fichero, "w", encoding="utf-8") as fichero:
            fichero.write(contenido_fichero)


if __name__ == '__main__':
    modulos=Modulo.objects.all().distinct()
    print(modulos)
    for m in modulos:
        codigo_modulo_segun_jccm=m.codigo_junta
        generar_fichero_corta_y_pega ( codigo_modulo_segun_jccm, DIRECTORIO_RESULTADOS )
        generar_lista_unidades_didacticas(m)                    
        
    



