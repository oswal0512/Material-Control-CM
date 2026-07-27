from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "cliente",
        "ubicacion",
        "fecha_inicio",
        "activo",
    )

    search_fields = (
        "nombre",
        "cliente",
    )

    list_filter = (
        "activo",
    )