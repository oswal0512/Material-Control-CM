from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.report_home,
        name="report_home"
    ),

    path(
        "inventario-pdf/",
        views.inventory_pdf,
        name="inventory_pdf"
    ),

    path(
        "entregas/",
        views.deliveries_report,
        name="deliveries_report"
    ),

    path(
    "inventario-excel/",
    views.inventory_excel,
    name="inventory_excel"
    ),

    path(
    "kardex-excel/",
    views.kardex_excel,
    name="kardex_excel"
    ),

    path(
    "entregas-excel/",
    views.deliveries_excel,
    name="deliveries_excel"
    ),

    path(
    "reporte-gerencial-pdf/",
    views.management_report_pdf,
    name="management_report_pdf"
    ),
]