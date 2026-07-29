from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        include("dashboard.urls")
    ),

    path(
        "materials/",
        include("materials.urls")
    ),

    path(
        "recepciones/",
        include("inventory.urls")
    ),

    path(
        "entregas/",
        include("movements.urls")
    ),

    path(
        "reportes/",
        include("reporting.urls")
    ),

    path(
        "kardex/",
        include("kardex.urls")
    ),

    path(
    "",
    include("accounts.urls"),
    ),

    path(
    "proveedores/",
    include("suppliers.urls")
    ),

]