from django import forms
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