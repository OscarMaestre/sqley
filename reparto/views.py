from django.shortcuts import render, get_object_or_404
from .models import RepartoForm, ModuloEnReparto, ModuloPorAsignar, ModuloAsignado, Reparto
from django.http import HttpResponseRedirect
from django.db import connection, transaction
from django.core.urlresolvers import reverse

EXTRACCION_MODULOS="""
SELECT mod.id, mod.nombre, mod.horas_semanales,
        g.nombre_grupo, ciclos.nivel_profesional, mod.especialidad
    from ciclos, modulos as mod, grupos as g, cursos as cur
        where
            mod.curso_id=cur.id
        and
            especialidad<>'PT'
        and
            g.curso_id=cur.id
        and
            cur.ciclo_id=ciclos.id
        
    order by horas_semanales desc, num_curso desc, nivel_profesional desc;
"""
# Create your views here.


def index(peticion):
    return render(None, "reparto/index.html")

def repartir(peticion, num_reparto, codigo_profesor, codigo_asignatura):
    return None

def crear_asignaturas_reparto ( id_reparto ):
    #print ("Creando para "+ str(id_reparto))
    reparto_asociado=get_object_or_404(Reparto, pk=id_reparto)
    with connection.cursor() as cursor:
        cursor.execute(EXTRACCION_MODULOS)
        filas=cursor.fetchall()
        with transaction.atomic():
            for f in filas:
                modulo_en_reparto=ModuloEnReparto(
                    nombre = f[1],
                    grupo = f[3],
                    horas_semanales=f[2],
                    especialidad=f[5],
                )
                modulo_en_reparto.save()
                modulo_por_asignar=ModuloPorAsignar(
                    modulo=modulo_en_reparto,reparto=reparto_asociado)
                modulo_por_asignar.save()
                #print (f[0])
    
def crear(peticion):
    if peticion.method=="POST":
        formulario_pasado=RepartoForm ( peticion.POST )
        if formulario_pasado.is_valid():
            formulario_pasado.save()
            id_reparto=formulario_pasado.instance.id
            ##print ( dir(formulario_pasado.instance))
            crear_asignaturas_reparto ( formulario_pasado.instance.id )
            return HttpResponseRedirect ( reverse("reparto:elegir",
                                                  args=(id_reparto,)
                                            )
                                        )
        else:
            print ("Meec")
    else:
        formulario=RepartoForm()
        datos={
            "formulario":formulario.as_table()
        }
        
        return render(peticion, "reparto/crear_reparto.html", datos)
    
def elegir ( peticion, num_reparto=None, num_profesor=None, num_asignatura=None ):
    datos={
        "num_reparto":num_reparto,
        "num_profesor":num_profesor,
        "num_asignatura":num_asignatura
    }
    return render ( peticion, "reparto/elegir.html", datos)
    