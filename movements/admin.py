from django.contrib import admin
from .models import (
    InventoryMovement,
    Delivery,
    DeliveryDetail
)


class DeliveryDetailInline(admin.TabularInline):
    model = DeliveryDetail
    extra = 1


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):

    list_display = (
    "id",
    "proyecto",
    "responsable",
    "fecha",
    "estado",
)

    inlines = [DeliveryDetailInline]


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):

    list_display = (
        "fecha",
        "material",
        "tipo",
        "cantidad",
        "saldo",
        "responsable",
    )

    list_filter = (
        "tipo",
    )

    search_fields = (
        "material__nombre",
        "referencia",
    )