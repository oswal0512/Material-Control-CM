from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Supplier
from .forms import SupplierForm

from accounts.decorators import almacen_required


@almacen_required
def supplier_list(request):

    buscar = request.GET.get("buscar", "")

    proveedores = Supplier.objects.all().order_by("razon_social")

    if buscar:

        proveedores = proveedores.filter(
            razon_social__icontains=buscar
        ) | Supplier.objects.filter(
            nombre_comercial__icontains=buscar
        ) | Supplier.objects.filter(
            nit__icontains=buscar
        )

    return render(
        request,
        "suppliers/list.html",
        {
            "proveedores": proveedores,
            "buscar": buscar,
        },
    )


@almacen_required
def supplier_create(request):

    if request.method == "POST":

        form = SupplierForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Proveedor creado correctamente."
            )

            return redirect("supplier_list")

    else:

        form = SupplierForm()

    return render(
        request,
        "suppliers/form.html",
        {
            "form": form
        }
    )


@almacen_required
def supplier_edit(request, pk):

    proveedor = get_object_or_404(
        Supplier,
        pk=pk
    )

    form = SupplierForm(
        request.POST or None,
        instance=proveedor
    )

    if request.method == "POST":

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Proveedor actualizado correctamente."
            )

            return redirect("supplier_list")

    return render(
        request,
        "suppliers/form.html",
        {
            "form": form
        }
    )


@almacen_required
def supplier_delete(request, pk):

    proveedor = get_object_or_404(
        Supplier,
        pk=pk
    )

    proveedor.activo = False

    proveedor.save()

    messages.success(
        request,
        "Proveedor desactivado correctamente."
    )

    return redirect(
        "supplier_list"
    )