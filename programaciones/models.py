from django.db import models

# Create your models here.


class UnidadDeTrabajo(models.Model):
    numero = models.IntegerField()
    nombre  =   models.CharField(max_length=180)
    sesiones = models.IntegerField()