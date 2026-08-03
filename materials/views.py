from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.contrib import messages
from decimal import Decimal

from inventory.models import ReceiptDetail
from movements.models import DeliveryDetail
from materials.models import Material


@staff_member_required
def recalcular_stock(request):

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

    messages.success(
        request,
        "✅ El stock de todos los materiales fue recalculado correctamente."
    )

    return redirect("material_list")