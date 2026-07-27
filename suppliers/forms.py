from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = [
            "nit",
            "razon_social",
            "nombre_comercial",
            "contacto",
            "cargo",
            "telefono",
            "celular",
            "correo",
            "direccion",
            "ciudad",
            "departamento",
            "observacion",
            "activo",
        ]

        widgets = {
            "observacion": forms.Textarea(
                attrs={"rows": 4}
            )
        }