from django.contrib import admin
from cat.models import Tarjeta, Movimiento, PagoPendiente, Moneda, Conversion


def define_balance(modeladmin, request, queryset):
    for tarjeta in queryset:
        tarjeta.define_balance()


@admin.register(Tarjeta)
class TarjetaAdmin(admin.ModelAdmin):
    list_display = (
        'numero',
        'rfc',
        'owner',
        'banco',
        'balance'
    )
    actions = [define_balance]


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_filter = (
        'tarjeta',
        'tipo'
    )
    list_display = (
        'tarjeta',
        'tipo',
        'concepto',
        'fecha'
    )


@admin.register(PagoPendiente)
class PagoPendienteAdmin(admin.ModelAdmin):
    list_filter = (
        'tarjeta',
    )
    list_display = (
        'tarjeta',
        'moneda',
        'cantidad_original',
        'concepto',
    )


admin.site.register((Moneda, Conversion),)