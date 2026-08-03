from django.urls import path
from . import views

urlpatterns = [
    path("", views.material_list, name="material_list"),
    path("nuevo/", views.material_create, name="material_create"),
    path("editar/<int:pk>/", views.material_update, name="material_update"),
    path("eliminar/<int:pk>/", views.material_delete, name="material_delete"),
    path("kardex/<int:pk>/", views.material_kardex, name="material_kardex"),
    path("recalcular-stock/", views.recalcular_stock, name="recalcular_stock",),
]
