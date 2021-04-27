from django import forms
from django.db import transaction

from cat.models import Movimiento, PagoPendiente, Tarjeta, Archivo


class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = (
            'rfc',
            'numero',
            'banco',
        )


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


class PagopendienteForm(forms.ModelForm):
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


class PagopendientePagarForm(forms.Form):
    adjunto = forms.FileField(required=False)

    def __init__(self, instancia, *args, **kwargs):
        self.pago_pendiente = instancia
        super(PagopendientePagarForm, self).__init__(*args, **kwargs)

    def save(self):
        pago_pendiente = self.pago_pendiente
        movimiento = pago_pendiente.pagar()
        with transaction.atomic():
            if pago_pendiente.pago_unico:
                pago_pendiente.estatus = PagoPendiente.PAGADO
                pago_pendiente.save()
            archivo = Archivo(file=self.cleaned_data['adjunto'])
            archivo.save()
            movimiento.adjunto = archivo
            movimiento.save()
        return pago_pendiente
