from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F

from .models import (
    Receipt,
    ReceiptDetail,
)

from movements.models import InventoryMovement

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

            Material = detalle.material.__class__

            Material.objects.filter(
                pk=detalle.material.pk
            ).update(
                stock=F("stock") + detalle.cantidad
            )

            detalle.material.refresh_from_db()

            InventoryMovement.objects.create(
                material=detalle.material,
                tipo="ENTRADA",
                cantidad=detalle.cantidad,
                saldo=detalle.material.stock,
                referencia=recepcion.numero_remision,
                responsable="ALMACEN",
                observacion="Recepción de material"
            )

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

    cantidad_anterior = detalle.cantidad

    form = ReceiptDetailForm(
        request.POST or None,
        instance=detalle
    )

    if request.method == "POST":

        if form.is_valid():

            nuevo = form.save(commit=False)

            diferencia = nuevo.cantidad - cantidad_anterior

            nuevo.save()

            Material = nuevo.material.__class__

            Material.objects.filter(
                pk=nuevo.material.pk
            ).update(
                stock=F("stock") + diferencia
            )

            nuevo.material.refresh_from_db()

            if diferencia != 0:

                InventoryMovement.objects.create(
                    material=nuevo.material,
                    tipo="ENTRADA" if diferencia > 0 else "SALIDA",
                    cantidad=abs(diferencia),
                    saldo=nuevo.material.stock,
                    referencia=recepcion.numero_remision,
                    responsable="ALMACEN",
                    observacion="Edición de recepción"
                )

            messages.success(
                request,
                "Detalle actualizado correctamente."
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
    cantidad = detalle.cantidad

    Material = material.__class__

    Material.objects.filter(
        pk=material.pk
    ).update(
        stock=F("stock") - cantidad
    )

    material.refresh_from_db()

    InventoryMovement.objects.create(
        material=material,
        tipo="SALIDA",
        cantidad=cantidad,
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