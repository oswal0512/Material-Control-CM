from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F

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

    entregas = Delivery.objects.all().order_by(
        "-fecha",
        "-id"
    )

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

            material.refresh_from_db()

            if material.stock < cantidad:

                messages.error(
                    request,
                    f"No existe stock suficiente. Disponible: {material.stock}"
                )

                return redirect(
                    "delivery_detail",
                    pk=pk
                )

            Material = material.__class__

            Material.objects.filter(
                pk=material.pk
            ).update(
                stock=F("stock") - cantidad
            )

            material.refresh_from_db()

            detalle.save()

            InventoryMovement.objects.create(
                material=material,
                tipo="SALIDA",
                cantidad=cantidad,
                saldo=material.stock,
                referencia=f"ENT-{entrega.id}",
                responsable=entrega.responsable,
                observacion="Entrega de material"
            )

            messages.success(
                request,
                "Material agregado correctamente."
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
        }
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
            "La entrega ya fue finalizada."
        )

        return redirect(
            "delivery_detail",
            pk=pk
        )

    entrega.estado = "FINALIZADA"

    entrega.save()

    messages.success(
        request,
        "Entrega finalizada correctamente."
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

    cantidad_anterior = detalle.cantidad

    form = DeliveryDetailForm(
        request.POST or None,
        instance=detalle
    )

    if request.method == "POST":

        if form.is_valid():

            nuevo = form.save(commit=False)

            diferencia = nuevo.cantidad - cantidad_anterior

            material = nuevo.material

            material.refresh_from_db()

            if diferencia > 0 and material.stock < diferencia:

                messages.error(
                    request,
                    f"No existe stock suficiente. Disponible: {material.stock}"
                )

                return redirect(
                    "delivery_detail",
                    pk=entrega.id
                )

            Material = material.__class__

            if diferencia > 0:

                Material.objects.filter(
                    pk=material.pk
                ).update(
                    stock=F("stock") - diferencia
                )

            elif diferencia < 0:

                Material.objects.filter(
                    pk=material.pk
                ).update(
                    stock=F("stock") + abs(diferencia)
                )

            material.refresh_from_db()

            nuevo.save()

            if diferencia != 0:

                InventoryMovement.objects.create(
                    material=material,
                    tipo="SALIDA" if diferencia > 0 else "ENTRADA",
                    cantidad=abs(diferencia),
                    saldo=material.stock,
                    referencia=f"ENT-{entrega.id}",
                    responsable=entrega.responsable,
                    observacion="Edición de entrega"
                )

            messages.success(
                request,
                "Detalle actualizado correctamente."
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

    cantidad = detalle.cantidad

    Material = material.__class__

    Material.objects.filter(
        pk=material.pk
    ).update(
        stock=F("stock") + cantidad
    )

    material.refresh_from_db()

    InventoryMovement.objects.create(
        material=material,
        tipo="ENTRADA",
        cantidad=cantidad,
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