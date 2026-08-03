from django.core.management.base import BaseCommand
from django.db.models import Sum
from decimal import Decimal

from materials.models import Material
from inventory.models import ReceiptDetail
from movements.models import DeliveryDetail


class Command(BaseCommand):
    help = "Recalcula el stock de todos los materiales."

    def handle(self, *args, **options):

        self.stdout.write("Recalculando stock...")

        # Reiniciar stock
        Material.objects.all().update(stock=Decimal("0.00"))

        for material in Material.objects.all():

            entradas = (
                ReceiptDetail.objects
                .filter(material=material)
                .aggregate(total=Sum("cantidad"))["total"]
                or Decimal("0.00")
            )

            salidas = (
                DeliveryDetail.objects
                .filter(material=material)
                .aggregate(total=Sum("cantidad"))["total"]
                or Decimal("0.00")
            )

            material.stock = entradas - salidas
            material.save(update_fields=["stock"])

            self.stdout.write(
                f"{material.codigo} - {material.nombre}: {material.stock}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                "✔ Stock recalculado correctamente."
            )
        )