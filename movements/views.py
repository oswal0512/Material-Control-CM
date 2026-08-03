from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Delivery,
    DeliveryDetail,
    InventoryMovement,
)

from .forms import (
    DeliveryForm,
    DeliveryDetailForm,
)
from accounts.decorators import (
    almacen_required,
    consulta_required,
)
@consulta_required
def delivery_list(request):

    entregas = Delivery.objects.all().order_by("-fecha", "-id")

    return render(
        request,
        "movements/list.html",
        {
            "entregas": entregas
        }
    )

@almacen_required
def delivery_create(request):

    if request.method == "POST":

        form = DeliveryForm(request.POST)

        if form.is_valid():

            entrega = form.save()

            messages.success(
                request,
                "Entrega creada correctamente."
            )

            return redirect(
                "delivery_detail",
                pk=entrega.pk
            )

    else:

        form = DeliveryForm()

    return render(
        request,
        "movements/form.html",
        {
            "form": form
        }
    )

@consulta_required
def delivery_detail(request, pk):

    entrega = get_object_or_404(
        Delivery,
        pk=pk
    )

    if request.method == "POST":

        if entrega.estado != "BORRADOR":

            messages.error(
                request,
                "La entrega ya fue finalizada."
            )

            return redirect(
                "delivery_detail",
                pk=pk
            )

        form = DeliveryDetailForm(request.POST)

        if form.is_valid():

            detalle = form.save(commit=False)

            detalle.entrega = entrega

            material = detalle.material

            cantidad = detalle.cantidad

            # Validar stock disponible
            if cantidad > material.stock:

                messages.error(
                    request,
                    f"❌ Stock insuficiente para '{material.nombre}'. "
                    f"Disponible: {material.stock} | "
                    f"Solicitado: {cantidad}"
                )

                return redirect(
                    "delivery_detail",
                    pk=pk
                )

            # Descontar inventario
            material.stock -= cantidad
            material.save()
            material.refresh_from_db()

            print("STOCK DESPUÉS DE GUARDAR:", material.stock)
            
            # Registrar movimiento de salida
            InventoryMovement.objects.create(
                material=material,
                tipo="SALIDA",
                cantidad=cantidad,
                saldo=material.stock,
                referencia=f"ENT-{entrega.id}",
                responsable=entrega.responsable,
                observacion="Entrega de material"
            )

            detalle.save()

            messages.success(
                request,
                "✅ Material agregado correctamente."
            )

            return redirect(
                "delivery_detail",
                pk=pk
            )

    else:

        form = DeliveryDetailForm()

    detalles = entrega.detalles.all()

    return render(
        request,
        "movements/detail.html",
        {
            "entrega": entrega,
            "form": form,
            "detalles": detalles,
        },
    )
@almacen_required
def delivery_finalize(request, pk):

    entrega = get_object_or_404(
        Delivery,
        pk=pk
    )

    if request.method != "POST":

        return redirect(
            "delivery_detail",
            pk=pk
        )

    if entrega.estado != "BORRADOR":

        messages.warning(
            request,
            "La entrega ya se encuentra finalizada."
        )

        return redirect(
            "delivery_detail",
            pk=pk
        )

    entrega.estado = "FINALIZADA"

    entrega.save()

    messages.success(
        request,
        "✅ La entrega fue finalizada correctamente."
    )

    return redirect(
        "delivery_detail",
        pk=pk
    )

@almacen_required
def delivery_detail_edit(request, pk):

    detalle = get_object_or_404(
        DeliveryDetail,
        pk=pk
    )

    entrega = detalle.entrega

    if entrega.estado != "BORRADOR":

        messages.error(
            request,
            "No se puede editar una entrega finalizada."
        )

        return redirect(
            "delivery_detail",
            pk=entrega.id
        )

    form = DeliveryDetailForm(
        request.POST or None,
        instance=detalle
    )

    if request.method == "POST":

        if form.is_valid():

            messages.info(
                request,
                "La edición de cantidades se implementará en el siguiente paso."
            )

            return redirect(
                "delivery_detail",
                pk=entrega.id
            )

    return render(
        request,
        "movements/form.html",
        {
            "form": form
        }
    )

@almacen_required
def delivery_detail_delete(request, pk):

    detalle = get_object_or_404(
        DeliveryDetail,
        pk=pk
    )

    entrega = detalle.entrega

    if entrega.estado != "BORRADOR":

        messages.error(
            request,
            "No se puede modificar una entrega finalizada."
        )

        return redirect(
            "delivery_detail",
            pk=entrega.id
        )

    material = detalle.material

    material.stock += detalle.cantidad

    material.save()

    InventoryMovement.objects.create(
        material=material,
        tipo="ENTRADA",
        cantidad=detalle.cantidad,
        saldo=material.stock,
        referencia=f"ELIM-ENT-{entrega.id}",
        responsable=entrega.responsable,
        observacion="Eliminación de detalle de entrega"
    )

    detalle.delete()

    messages.success(
        request,
        "Material eliminado correctamente."
    )

    return redirect(
        "delivery_detail",
        pk=entrega.id
    )