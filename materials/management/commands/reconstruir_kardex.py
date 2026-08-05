from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from materials.models import Material

from inventory.models import ReceiptDetail

from movements.models import (
    DeliveryDetail,
    InventoryMovement,
)


class Command(BaseCommand):

    help = "Reconstruye completamente el Kardex y sincroniza el inventario."

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write(
            self.style.WARNING(
                "Iniciando reconstrucción de Kardex..."
            )
        )


        # -----------------------------------------
        # 1. Limpiar movimientos actuales
        # -----------------------------------------

        eliminados = InventoryMovement.objects.count()

        InventoryMovement.objects.all().delete()


        self.stdout.write(
            self.style.SUCCESS(
                f"Movimientos eliminados: {eliminados}"
            )
        )


        # -----------------------------------------
        # 2. Reiniciar stock
        # -----------------------------------------

        Material.objects.all().update(
            stock=Decimal("0.00")
        )


        materiales = {
            material.id: material
            for material in Material.objects.all()
        }


        total_entradas = Decimal("0.00")
        total_salidas = Decimal("0.00")

        movimientos = 0


        # -----------------------------------------
        # 3. Reconstruir entradas
        # -----------------------------------------

        recepciones = ReceiptDetail.objects.select_related(
            "material",
            "recepcion",
        ).order_by(
            "recepcion__fecha",
            "recepcion__id",
            "id",
        )


        for detalle in recepciones:

            material = materiales[
                detalle.material_id
            ]

            material.stock += detalle.cantidad

            material.save(
                update_fields=[
                    "stock"
                ]
            )


            fecha = timezone.make_aware(
                timezone.datetime.combine(
                    detalle.recepcion.fecha,
                    timezone.datetime.min.time()
                )
            )


            InventoryMovement.objects.create(
                material=material,
                fecha=fecha,
                tipo="ENTRADA",
                cantidad=detalle.cantidad,
                saldo=material.stock,
                referencia=detalle.recepcion.numero_remision,
                responsable="ALMACEN",
                observacion="Reconstrucción desde recepción"
            )


            total_entradas += detalle.cantidad
            movimientos += 1



        self.stdout.write(
            self.style.SUCCESS(
                f"Entradas reconstruidas: {total_entradas}"
            )
        )



        # -----------------------------------------
        # 4. Reconstruir salidas
        # -----------------------------------------

        entregas = DeliveryDetail.objects.select_related(
            "material",
            "entrega",
        ).order_by(
            "entrega__fecha",
            "entrega__id",
            "id",
        )


        for detalle in entregas:

            material = materiales[
                detalle.material_id
            ]


            material.stock -= detalle.cantidad


            material.save(
                update_fields=[
                    "stock"
                ]
            )


            fecha = timezone.make_aware(
                timezone.datetime.combine(
                    detalle.entrega.fecha,
                    timezone.datetime.max.time()
                )
            )


            InventoryMovement.objects.create(
                material=material,
                fecha=fecha,
                tipo="SALIDA",
                cantidad=detalle.cantidad,
                saldo=material.stock,
                referencia=f"ENT-{detalle.entrega.id}",
                responsable=detalle.entrega.responsable,
                observacion="Reconstrucción desde entrega"
            )


            total_salidas += detalle.cantidad
            movimientos += 1



        self.stdout.write(
            self.style.SUCCESS(
                f"Salidas reconstruidas: {total_salidas}"
            )
        )



        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "KARDEX RECONSTRUIDO CORRECTAMENTE"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total movimientos creados: {movimientos}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Stock sincronizado con recepciones y entregas."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )