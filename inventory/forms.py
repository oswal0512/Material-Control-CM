from django import forms
from .models import Receipt, ReceiptDetail
from django import forms
from .models import Receipt, ReceiptDetail
from materials.models import Material


class ReceiptForm(forms.ModelForm):

    class Meta:
        model = Receipt
        fields = [
            "proyecto",
            "proveedor",
            "numero_remision",
            "fecha",
        ]

class ReceiptForm(forms.ModelForm):

    class Meta:
        model = Receipt
        fields = "__all__"


class ReceiptDetailForm(forms.ModelForm):

    class Meta:
        model = ReceiptDetail
        fields = [
            "material",
            "cantidad",
        ]

        widgets = {
            "material": forms.Select(
                attrs={
                    "class": "form-select select2",
                }
            ),
            "cantidad": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["material"].queryset = Material.objects.filter(
            activo=True
        ).order_by("codigo")

        self.fields["material"].label_from_instance = (
            lambda obj: f"{obj.codigo} | {obj.nombre}"
        )