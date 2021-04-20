from django import forms

from cat.models import Movimiento, PagoPendiente


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = (
            'cantidad_original',
            'moneda',
            'tipo',
            'concepto',
            'adjunto'
        )


class PagoPendienteForm(forms.ModelForm):
    class Meta:
        model = PagoPendiente
        fields = (
            'cantidad_original',
            'moneda',
            'concepto',
            'pago_automatico',
            'pago_unico',
            'periodicidad',
            'programacion',
        )