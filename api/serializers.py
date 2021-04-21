from django.db import transaction

from cat.models import Tarjeta, Movimiento
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

    def get_owner_name(self, instance):
        return instance.owner.username

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
    class Meta:
        model = Movimiento
        fields = (
            'id',
            'abono_pendiente',
            'moneda',
            'cantidad_original',
            'tarjeta',
            'cantidad',
            'tipo',
            'adjunto',
            'concepto',
            'get_tipo_display',
        )
