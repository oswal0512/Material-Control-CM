from django.db import models


class Project(models.Model):
    nombre = models.CharField(max_length=150)
    cliente = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre