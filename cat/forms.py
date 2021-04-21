from django import forms

from cat.models import Tarjeta


class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = (
            'rfc',
            'numero',
            'banco',
        )