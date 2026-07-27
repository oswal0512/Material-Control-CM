from django.db import models
from projects.models import Project
from materials.models import Material
from suppliers.models import Supplier


class Receipt(models.Model):
    proyecto = models.ForeignKey(Project, on_delete=models.CASCADE)
    proveedor = models.CharField(
    max_length=200
)
    numero_remision = models.CharField(max_length=100)
    fecha = models.DateField()

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


    def save(self, *args, **kwargs):

        from movements.models import InventoryMovement

        if self.pk:

            anterior = ReceiptDetail.objects.get(
                pk=self.pk
            )

            diferencia = (
                self.cantidad -
                anterior.cantidad
            )

            super().save(*args, **kwargs)

            if diferencia != 0:

                self.material.stock += diferencia

                self.material.save()

                InventoryMovement.objects.create(
                    material=self.material,
                    tipo="ENTRADA" if diferencia > 0 else "SALIDA",
                    cantidad=abs(diferencia),
                    saldo=self.material.stock,
                    referencia=self.recepcion.numero_remision,
                    responsable="ALMACEN",
                    observacion="Ajuste por edición de recepción"
                )

        else:

            super().save(*args, **kwargs)

            self.material.stock += self.cantidad

            self.material.save()

            InventoryMovement.objects.create(
                material=self.material,
                tipo="ENTRADA",
                cantidad=self.cantidad,
                saldo=self.material.stock,
                referencia=self.recepcion.numero_remision,
                responsable="ALMACEN",
                observacion="Recepción de material"
            )


    def __str__(self):

        return self.material.nombre