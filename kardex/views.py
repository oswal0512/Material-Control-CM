from django.shortcuts import render

from movements.models import InventoryMovement
from materials.models import Material

from accounts.decorators import consulta_required


@almacen_required
def kardex_list(request):

    material_id = request.GET.get("material")

    fecha_inicio = request.GET.get("fecha_inicio")

    fecha_fin = request.GET.get("fecha_fin")

    movimientos = InventoryMovement.objects.all().order_by(
        "-fecha"
    )

    if material_id:

        movimientos = movimientos.filter(
            material_id=material_id
        )

    if fecha_inicio:

        movimientos = movimientos.filter(
            fecha__gte=fecha_inicio
        )

    if fecha_fin:

        movimientos = movimientos.filter(
            fecha__lte=fecha_fin
        )

    materiales = Material.objects.filter(
        activo=True
    ).order_by(
        "nombre"
    )

    context = {

        "movimientos": movimientos,

        "materiales": materiales,

        "material_seleccionado": material_id,

        "fecha_inicio": fecha_inicio,

        "fecha_fin": fecha_fin,

    }

    return render(
        request,
        "kardex/list.html",
        context
    )