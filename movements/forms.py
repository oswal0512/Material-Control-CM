from django import forms
from materials.models import Material
from .models import Delivery, DeliveryDetail


class DeliveryForm(forms.ModelForm):

    class Meta:
        model = Delivery
        fields = [
            "proyecto",
            "responsable",
            "fecha",
            "observacion",
        ]


class DeliveryDetailForm(forms.ModelForm):

    class Meta:
        model = DeliveryDetail
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
        