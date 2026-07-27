from django.db import models


class Employee(models.Model):

    CARGOS = (
        ("ALMACENISTA", "Almacenista"),
        ("RESIDENTE", "Residente"),
        ("SUPERVISOR CIVIL", "Supervisor Civil"),
        ("SUPERVISOR ELECTRICO", "Supervisor Eléctrico"),
        ("SUPERVISOR MECANICO", "Supervisor Mecánico"),
    )

    codigo = models.CharField(
        max_length=20,
        unique=True
    )

    nombre = models.CharField(
        max_length=150
    )

    cargo = models.CharField(
        max_length=30,
        choices=CARGOS
    )

    activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.nombre} ({self.cargo})"