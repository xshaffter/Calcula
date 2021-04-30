from django.db import transaction

from cat.models import Tarjeta, Movimiento, PagoPendiente, AbonoPendiente
from rest_framework import serializers


class HeaderSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    display = serializers.CharField(max_length=100, required=True)
    type = serializers.CharField(max_length=100, required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ModelDataSerializer(serializers.Serializer):
    headers = HeaderSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class TarjetaSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()
    numero = serializers.SerializerMethodField()

    def get_owner_name(self, instance):
        return instance.owner.username

    def get_numero(self, instance):
        return instance.get_tarjeta_display()

    class Meta:
        model = Tarjeta
        fields = (
            'id',
            'owner_name',
            'rfc',
            'numero',
            'banco',
            'balance',
            'actions'
        )


class MovimientoSerializer(serializers.ModelSerializer):
    moneda_display = serializers.SerializerMethodField()

    def get_moneda_display(self, obj):
        return obj.moneda.nombre_corto

    class Meta:
        model = Movimiento
        fields = (
            'id',
            'tarjeta',
            'abono_pendiente',
            'moneda',
            'moneda_display',
            'cantidad_original',
            'tarjeta',
            'cantidad',
            'tipo',
            'adjunto',
            'concepto',
            'get_tipo_display',
            'actions'
        )


class PagoPendienteSerializer(serializers.ModelSerializer):
    moneda_display = serializers.SerializerMethodField()

    def get_moneda_display(self, obj):
        return obj.moneda.nombre_corto

    class Meta:
        model = PagoPendiente
        fields = (
            'id',
            'tarjeta',
            'cantidad_original',
            'moneda',
            'moneda_display',
            'concepto',
            'pago_automatico',
            'get_estatus_display',
            'actions'
        )


class AbonoPendienteSerializer(serializers.ModelSerializer):
    moneda_display = serializers.SerializerMethodField()

    def get_moneda_display(self, obj):
        return obj.moneda.nombre_corto

    class Meta:
        model = AbonoPendiente
        fields = (
            'id',
            'tarjeta',
            'cantidad_original',
            'moneda',
            'moneda_display',
            'concepto',
            'pago_automatico',
            'get_estatus_display',
            'actions'
        )
