from django.db import models

from projects.models import Project
from materials.models import Material


class Receipt(models.Model):

    proyecto = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    proveedor = models.CharField(
        max_length=200
    )

    numero_remision = models.CharField(
        max_length=100
    )

    fecha = models.DateField()

    class Meta:
        ordering = ["-fecha", "-id"]
        verbose_name = "Recepción"
        verbose_name_plural = "Recepciones"

    def __str__(self):
        return f"{self.numero_remision} - {self.proveedor}"


class ReceiptDetail(models.Model):

    recepcion = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE
    )

    cantidad = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    observacion = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Detalle de Recepción"
        verbose_name_plural = "Detalles de Recepción"

    def __str__(self):
        return f"{self.material.nombre} ({self.cantidad})"