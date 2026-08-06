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
from django.db.models import Q
from materials.models import Material


@consulta_required
def receipt_list(request):

    buscar = request.GET.get("buscar", "")
    proyecto = request.GET.get("proyecto", "")
    fecha_inicio = request.GET.get("fecha_inicio", "")
    fecha_fin = request.GET.get("fecha_fin", "")

    recepciones = Receipt.objects.all()

    if buscar:

        recepciones = recepciones.filter(

            Q(proveedor__icontains=buscar) |
            Q(numero_remision__icontains=buscar)

        )

    if proyecto:

        recepciones = recepciones.filter(
            proyecto_id=proyecto
        )

    if fecha_inicio:

        recepciones = recepciones.filter(
            fecha__gte=fecha_inicio
        )

    if fecha_fin:

        recepciones = recepciones.filter(
            fecha__lte=fecha_fin
        )

    from projects.models import Project

    proyectos = Project.objects.order_by("nombre")

    recepciones = recepciones.order_by(
        "-fecha",
        "-id"
    )

    return render(
        request,
        "inventory/list.html",
        {
            "recepciones": recepciones,
            "buscar": buscar,
            "proyectos": proyectos,
            "proyecto": proyecto,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
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

    if request.method == "POST":

        form = ReceiptDetailForm(
            request.POST,
            instance=detalle
        )

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

    else:

        form = ReceiptDetailForm(instance=detalle)

    return render(
        request,
        "inventory/form.html",
        {
            "form": form,
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

    buscar = request.GET.get("buscar", "")
    estado = request.GET.get("estado", "")

    materiales = Material.objects.filter(activo=True)

    if buscar:

        materiales = materiales.filter(

            Q(codigo__icontains=buscar) |
            Q(nombre__icontains=buscar)

        )

    if estado == "con":

        materiales = materiales.filter(
            stock__gt=0
        )

    elif estado == "sin":

        materiales = materiales.filter(
            stock__lte=0
        )

    materiales = materiales.order_by(
        "nombre"
    )

    return render(
        request,
        "inventory/inventory.html",
        {
            "materiales": materiales,
            "buscar": buscar,
            "estado": estado,
        }
    )