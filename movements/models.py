from django.db import models
from django.core.exceptions import ValidationError

from materials.models import Material
from projects.models import Project


class InventoryMovement(models.Model):

    TIPOS = (
        ("ENTRADA", "Entrada"),
        ("SALIDA", "Salida"),
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPOS
    )

    cantidad = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    saldo = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    referencia = models.CharField(
        max_length=100,
        blank=True
    )

    responsable = models.CharField(
        max_length=150,
        blank=True
    )

    observacion = models.TextField(
        blank=True
    )

    class Meta:

        ordering = ["-fecha"]

        verbose_name = "Movimiento de Inventario"

        verbose_name_plural = "Movimientos de Inventario"

    def __str__(self):

        return f"{self.tipo} - {self.material.nombre}"


class Delivery(models.Model):

    ESTADOS = (

        ("BORRADOR", "Borrador"),

        ("FINALIZADA", "Finalizada"),

        ("ANULADA", "Anulada"),

    )

    proyecto = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    responsable = models.CharField(
        max_length=150
    )

    fecha = models.DateField()

    observacion = models.TextField(
        blank=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="BORRADOR"
    )

    class Meta:

        ordering = ["-fecha", "-id"]

        verbose_name = "Entrega"

        verbose_name_plural = "Entregas"

    def __str__(self):

        return f"Entrega #{self.id}"


class DeliveryDetail(models.Model):

    entrega = models.ForeignKey(
        Delivery,
        related_name="detalles",
        on_delete=models.CASCADE
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE
    )

    cantidad = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    class Meta:

        verbose_name = "Detalle de Entrega"

        verbose_name_plural = "Detalles de Entrega"

    from materials.models import Material

def save(self, *args, **kwargs):

    material_bd = Material.objects.get(pk=self.material.pk)

    print("================================")
    print("OBJETO FORMULARIO :", self.material.stock)
    print("OBJETO BASE DATOS :", material_bd.stock)
    print("MATERIAL:", material_bd.nombre)
    print("================================")

    nuevo = self.pk is None
    def __str__(self):

        return f"{self.material.nombre} ({self.cantidad})"