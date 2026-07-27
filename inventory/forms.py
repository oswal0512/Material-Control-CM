from django import forms
from .models import Receipt, ReceiptDetail


class ReceiptForm(forms.ModelForm):

    class Meta:
        model = Receipt
        fields = [
            "proyecto",
            "proveedor",
            "numero_remision",
            "fecha",
        ]


class ReceiptDetailForm(forms.ModelForm):

    class Meta:
        model = ReceiptDetail
        fields = [
            "material",
            "cantidad",
            "observacion",
        ]