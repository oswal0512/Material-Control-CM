from django.core.management.base import BaseCommand
from django.db import transaction

from materials.models import Material
from inventory.models import ReceiptDetail
from movements.models import DeliveryDetail


class Command(BaseCommand):
    help = "Recalcula el stock de materiales basado en recepciones y entregas existentes."

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write(
            self.style.WARNING(
                "Iniciando recalculo de inventario..."
            )
        )

        # 1. Reiniciar stock de todos los materiales
        materiales = Material.objects.all()

        for material in materiales:
            material.stock = 0
            material.save(update_fields=["stock"])

        self.stdout.write(
            self.style.SUCCESS(
                "Stock inicializado en cero."
            )
        )

        # 2. Sumar todas las recepciones
        recepciones = ReceiptDetail.objects.select_related(
            "material"
        ).all()

        total_recibido = 0

        for detalle in recepciones:

            material = detalle.material

            material.stock += detalle.cantidad
            material.save(update_fields=["stock"])

            total_recibido += detalle.cantidad


        self.stdout.write(
            self.style.SUCCESS(
                f"Recepciones procesadas: {total_recibido}"
            )
        )


        # 3. Restar todas las entregas
        entregas = DeliveryDetail.objects.select_related(
            "material"
        ).all()

        total_entregado = 0

        for detalle in entregas:

            material = detalle.material

            material.stock -= detalle.cantidad
            material.save(update_fields=["stock"])

            total_entregado += detalle.cantidad


        self.stdout.write(
            self.style.SUCCESS(
                f"Entregas procesadas: {total_entregado}"
            )
        )


        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Inventario recalculado correctamente."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "El stock ahora coincide con los movimientos reales."
            )
        )