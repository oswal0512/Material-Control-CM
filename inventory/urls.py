from django.urls import path

from . import views
from . import reports


urlpatterns = [

    path(
        "",
        views.receipt_list,
        name="receipt_list"
    ),

    path(
        "nuevo/",
        views.receipt_create,
        name="receipt_create"
    ),

    path(
        "<int:pk>/",
        views.receipt_detail,
        name="receipt_detail"
    ),

    # -------------------------
    # REPORTES
    # -------------------------

    path(
        "<int:pk>/pdf/",
        reports.receipt_pdf,
        name="receipt_pdf"
    ),

    path(
        "<int:pk>/excel/",
        reports.receipt_excel,
        name="receipt_excel"
    ),

    # -------------------------
    # DETALLES
    # -------------------------

    path(
        "detalle/<int:pk>/editar/",
        views.receipt_detail_edit,
        name="receipt_detail_edit"
    ),

    path(
        "detalle/<int:pk>/eliminar/",
        views.receipt_detail_delete,
        name="receipt_detail_delete"
    ),

    path(
    "inventario/",
    views.inventory_list,
    name="inventory_list"
),

]