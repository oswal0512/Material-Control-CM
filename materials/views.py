from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Material
from .forms import MaterialForm
from movements.models import InventoryMovement
from accounts.decorators import (
    almacen_required,
    consulta_required,
    almacen_consulta_required,
)
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from inventory.models import ReceiptDetail
from movements.models import DeliveryDetail

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

@consulta_required
def material_list(request):

    buscar = request.GET.get("buscar", "")

    estado = request.GET.get("estado", "1")

    materiales = Material.objects.all()

    # -------------------------------
    # Filtro por estado
    # -------------------------------

    if estado == "1":
        materiales = materiales.filter(activo=True)

    elif estado == "0":
        materiales = materiales.filter(activo=False)

    # -------------------------------
    # Filtro por código o nombre
    # -------------------------------

    if buscar:

        materiales = materiales.filter(

            Q(codigo__icontains=buscar) |
            Q(nombre__icontains=buscar)

        )

    materiales = materiales.order_by("codigo")

    paginator = Paginator(
        materiales,
        10
    )

    page = request.GET.get("page")

    materiales = paginator.get_page(page)

    return render(
        request,
        "materials/list.html",
        {
            "materiales": materiales,
            "buscar": buscar,
            "estado": estado,
        },
    )

@almacen_required
def material_create(request):

    if request.method == "POST":

        form = MaterialForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("material_list")

    else:

        form = MaterialForm()

    return render(
        request,
        "materials/form.html",
        {
            "form": form,
        },
    )

@almacen_required
def material_update(request, pk):

    material = get_object_or_404(Material, pk=pk)

    if request.method == "POST":

        form = MaterialForm(
            request.POST,
            instance=material,
        )

        if form.is_valid():
            form.save()
            return redirect("material_list")

    else:

        form = MaterialForm(instance=material)

    return render(
        request,
        "materials/form.html",
        {
            "form": form,
        },
    )

@almacen_required
def material_delete(request, pk):

    material = get_object_or_404(Material, pk=pk)

    material.activo = False
    material.save()

    return redirect("material_list")

@consulta_required
def material_kardex(request, pk):

    material = get_object_or_404(Material, pk=pk)

    movimientos = (
        InventoryMovement.objects
        .filter(material_id=pk)
        .order_by("-fecha", "-id")
    )

    return render(
        request,
        "materials/kardex.html",
        {
            "material": material,
            "movimientos": movimientos,
        },
    )
