from django.contrib import admin
from .models import Receipt, ReceiptDetail


class ReceiptDetailInline(admin.TabularInline):
    model = ReceiptDetail
    extra = 1


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "numero_remision",
        "proveedor",
        "proyecto",
        "fecha",
    )

    inlines = [ReceiptDetailInline]