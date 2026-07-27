from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Material
from .forms import MaterialForm
from movements.models import InventoryMovement
from accounts.decorators import almacen_required


@almacen_required
def material_list(request):

    ...

    buscar = request.GET.get("buscar", "")

    materiales = Material.objects.filter(activo=True)

    if buscar:
        materiales = materiales.filter(
            Q(codigo__icontains=buscar) |
            Q(nombre__icontains=buscar)
        )

    paginator = Paginator(materiales.order_by("codigo"), 10)

    page = request.GET.get("page")

    materiales = paginator.get_page(page)

    return render(
        request,
        "materials/list.html",
        {
            "materiales": materiales,
            "buscar": buscar,
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

@almacen_required
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