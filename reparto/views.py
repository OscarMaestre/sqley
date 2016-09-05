from django.shortcuts import render

# Create your views here.


def index(peticion):
    return render(None, "reparto/index.html")

def repartir(peticion, num_reparto, codigo_profesor, codigo_asignatura):
    return None

def crear(peticion):
    return render(None, "reparto/crear_reparto.html")