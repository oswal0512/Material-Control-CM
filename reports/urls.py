from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.report_home,
        name="report_home"
    ),

    path(
        "inventario/",
        views.inventory_report,
        name="inventory_report"
    ),

    path(
        "inventario/excel/",
        views.inventory_excel,
        name="inventory_excel"
    ),

]