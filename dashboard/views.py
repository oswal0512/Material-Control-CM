from django.shortcuts import render
from django.db.models import Count

from materials.models import Material
from inventory.models import Receipt
from movements.models import (
    Delivery,
    InventoryMovement,
)
from django.contrib.auth.decorators import login_required

@login_required

def home(request):

    total_materiales = Material.objects.filter(
        activo=True
    ).count()

    total_recepciones = Receipt.objects.count()

    total_entregas = Delivery.objects.count()

    total_movimientos = InventoryMovement.objects.count()

    stock_bajo = Material.objects.filter(
        activo=True,
        stock__lte=10
    ).count()

    movimientos_recientes = InventoryMovement.objects.order_by(
        "-fecha"
    )[:5]

    ultimas_entregas = Delivery.objects.order_by(
        "-fecha",
        "-id"
    )[:5]

    ultimas_recepciones = Receipt.objects.order_by(
        "-fecha",
        "-id"
    )[:5]

    materiales_stock_bajo = Material.objects.filter(
        activo=True,
        stock__lte=10
    ).order_by("stock")[:5]

    tipos_movimiento = InventoryMovement.objects.values(
        "tipo"
    ).annotate(
        total=Count("id")
    )

    entradas = 0
    salidas = 0

    for item in tipos_movimiento:

        if item["tipo"] == "ENTRADA":
            entradas = item["total"]

        elif item["tipo"] == "SALIDA":
            salidas = item["total"]

    context = {

        "total_materiales": total_materiales,
        "total_recepciones": total_recepciones,
        "total_entregas": total_entregas,
        "total_movimientos": total_movimientos,
        "stock_bajo": stock_bajo,

        "movimientos_recientes": movimientos_recientes,
        "ultimas_entregas": ultimas_entregas,
        "ultimas_recepciones": ultimas_recepciones,
        "materiales_stock_bajo": materiales_stock_bajo,

        "entradas": entradas,
        "salidas": salidas,

    }

    return render(
        request,
        "dashboard.html",
        context
    )