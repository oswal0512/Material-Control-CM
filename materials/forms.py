from django import forms
from .models import Material


class MaterialForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = [
            "codigo",
            "nombre",
            "unidad",
            "stock",
            "activo",
        ]