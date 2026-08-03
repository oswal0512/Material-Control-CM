from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Receipt,
    ReceiptDetail,
)

from .forms import (
    ReceiptForm,
    ReceiptDetailForm,
)
from accounts.decorators import (
    almacen_required,
    consulta_required,
)
@consulta_required
def receipt_list(request):

    recepciones = Receipt.objects.all().order_by(
        "-fecha",
        "-id"
    )

    return render(
        request,
        "inventory/list.html",
        {
            "recepciones": recepciones
        }
    )

@almacen_required
def receipt_create(request):

    if request.method == "POST":

        form = ReceiptForm(request.POST)

        if form.is_valid():

            recepcion = form.save()

            messages.success(
                request,
                "Recepción creada correctamente."
            )

            return redirect(
                "receipt_detail",
                pk=recepcion.pk
            )

    else:

        form = ReceiptForm()

    return render(
        request,
        "inventory/form.html",
        {
            "form": form
        }
    )

@consulta_required
def receipt_detail(request, pk):

    recepcion = get_object_or_404(
        Receipt,
        pk=pk
    )

    if request.method == "POST":

        form = ReceiptDetailForm(request.POST)

        if form.is_valid():

            detalle = form.save(commit=False)

            detalle.recepcion = recepcion

            detalle.save()

            messages.success(
                request,
                "Material agregado correctamente."
            )

            return redirect(
                "receipt_detail",
                pk=pk
            )

    else:

        form = ReceiptDetailForm()

    detalles = recepcion.detalles.all()

    return render(
        request,
        "inventory/detail.html",
        {
            "recepcion": recepcion,
            "detalles": detalles,
            "form": form,
        },
    )
@almacen_required
def receipt_detail_edit(request, pk):

    detalle = get_object_or_404(
        ReceiptDetail,
        pk=pk
    )

    recepcion = detalle.recepcion

    form = ReceiptDetailForm(
        request.POST or None,
        instance=detalle
    )

    if request.method == "POST":

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Detalle de recepción actualizado correctamente."
            )

            return redirect(
                "receipt_detail",
                pk=recepcion.id
            )


    return render(
        request,
        "inventory/form.html",
        {
            "form": form
        }
    )
@almacen_required
def receipt_detail_delete(request, pk):

    detalle = get_object_or_404(
        ReceiptDetail,
        pk=pk
    )

    material = detalle.material

    recepcion = detalle.recepcion


    material.stock -= detalle.cantidad

    material.save()


    from movements.models import InventoryMovement


    InventoryMovement.objects.create(

        material=material,

        tipo="SALIDA",

        cantidad=detalle.cantidad,

        saldo=material.stock,

        referencia=f"ANULACION-{recepcion.numero_remision}",

        responsable="ALMACEN",

        observacion="Eliminación de detalle de recepción"

    )


    detalle.delete()


    messages.success(
        request,
        "Material eliminado de la recepción correctamente."
    )


    return redirect(
        "receipt_detail",
        pk=recepcion.id
    )
@consulta_required
def inventory_list(request):

    from materials.models import Material


    materiales = Material.objects.filter(
        activo=True
    ).order_by(
        "nombre"
    )


    return render(
        request,
        "inventory/inventory.html",
        {
            "materiales": materiales
        }
    )