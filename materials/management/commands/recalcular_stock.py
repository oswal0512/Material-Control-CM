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
        help = "Recalcula el stock de todos los materiales."

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write(
            self.style.WARNING(
                "Reconstruyendo inventario y kardex..."
            )
        )

        # -------------------------------------------------
        # Eliminar Kardex
        # -------------------------------------------------

        InventoryMovement.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Kardex eliminado."
            )
        )

        # -------------------------------------------------
        # Reiniciar Stock
        # -------------------------------------------------

        Material.objects.all().update(
            stock=Decimal("0.00")
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Stock inicializado en cero."
            )
        )

        materiales = {
            m.id: m
            for m in Material.objects.all()
        }

        movimientos = 0
        total_recibido = Decimal("0.00")
        total_entregado = Decimal("0.00")

        # -------------------------------------------------
        # RECEPCIONES
        # -------------------------------------------------

        recepciones = (
            ReceiptDetail.objects
            .select_related(
                "material",
                "recepcion",
            )
            .order_by(
                "recepcion__fecha",
                "recepcion__id",
                "id",
            )
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

            InventoryMovement.objects.create(
                material=material,
                fecha=timezone.make_aware(
                    timezone.datetime.combine(
                        detalle.recepcion.fecha,
                        timezone.datetime.min.time()
                    )
                ),
                tipo="ENTRADA",
                cantidad=detalle.cantidad,
                saldo=material.stock,
                referencia=detalle.recepcion.numero_remision,
                responsable="ALMACEN",
                observacion="Recepción de material"
            )

            movimientos += 1

            total_recibido += detalle.cantidad

        self.stdout.write(
            self.style.SUCCESS(
                f"Recepciones procesadas: {total_recibido}"
            )
        )

        # -------------------------------------------------
        # ENTREGAS
        # -------------------------------------------------

        entregas = (
            DeliveryDetail.objects
            .select_related(
                "material",
                "entrega",
            )
            .order_by(
                "entrega__fecha",
                "entrega__id",
                "id",
            )
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

            InventoryMovement.objects.create(
                material=material,
                fecha=timezone.make_aware(
                    timezone.datetime.combine(
                        detalle.entrega.fecha,
                        timezone.datetime.max.time().replace(microsecond=0)
                    )
                ),
                tipo="SALIDA",
                cantidad=detalle.cantidad,
                saldo=material.stock,
                referencia=f"ENT-{detalle.entrega.id}",
                responsable=detalle.entrega.responsable,
                observacion="Entrega de material"
            )

            movimientos += 1

            total_entregado += detalle.cantidad

        self.stdout.write(
            self.style.SUCCESS(
                f"Entregas procesadas: {total_entregado}"
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
                f"Movimientos creados: {movimientos}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "Stock sincronizado correctamente."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )