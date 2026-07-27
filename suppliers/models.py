from django.db import models


class Supplier(models.Model):

    nit = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="NIT"
    )

    razon_social = models.CharField(
        max_length=200,
        verbose_name="Razón Social"
    )

    nombre_comercial = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Nombre Comercial"
    )

    contacto = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Contacto"
    )

    cargo = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Cargo"
    )

    telefono = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Teléfono"
    )

    celular = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Celular"
    )

    correo = models.EmailField(
        blank=True,
        verbose_name="Correo Electrónico"
    )

    direccion = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Dirección"
    )

    ciudad = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Ciudad"
    )

    departamento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Departamento"
    )

    observacion = models.TextField(
        blank=True,
        verbose_name="Observaciones"
    )

    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "razon_social"
        ]

        verbose_name = "Proveedor"

        verbose_name_plural = "Proveedores"

    def __str__(self):

        return f"{self.nit} - {self.razon_social}"