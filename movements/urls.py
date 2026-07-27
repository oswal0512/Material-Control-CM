from django.urls import path

from . import views
from . import reports


urlpatterns = [

    path(
        "",
        views.delivery_list,
        name="delivery_list"
    ),

    path(
        "nuevo/",
        views.delivery_create,
        name="delivery_create"
    ),

    path(
        "<int:pk>/",
        views.delivery_detail,
        name="delivery_detail"
    ),

    path(
        "<int:pk>/finalizar/",
        views.delivery_finalize,
        name="delivery_finalize"
    ),

    path(
        "detalle/<int:pk>/editar/",
        views.delivery_detail_edit,
        name="delivery_detail_edit"
    ),

    path(
        "detalle/<int:pk>/eliminar/",
        views.delivery_detail_delete,
        name="delivery_detail_delete"
    ),

    path(
        "<int:pk>/pdf/",
        reports.delivery_pdf,
        name="delivery_pdf"
    ),

    path(
    "<int:pk>/excel/",
    reports.delivery_excel,
    name="delivery_excel"
),

]