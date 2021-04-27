import base64
import json

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.paginators import ShortResultsSetPagination
from api.serializers import PagoPendienteSerializer
from cat.models import PagoPendiente


class PagoPendienteViewSet(viewsets.ModelViewSet):
    queryset = PagoPendiente.objects.all()
    serializer_class = PagoPendienteSerializer
    pagination_class = ShortResultsSetPagination

    def list(self, request, *args, **kwargs):
        tarjeta = request.GET.get('parent_id')
        queryset = self.queryset.filter(tarjeta_id=tarjeta).exclude(estatus=PagoPendiente.PAGADO)
        serializer = self.get_serializer(instance=queryset, many=True)
        pagination = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(pagination)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=json.loads(request.data['data']))
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.queryset.get(pk=pk)
        serializer = self.serializer_class(instance, data=json.loads(request.data['data']), partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'put'])
    def pagar(self, request, pk=None, *args, **kwargs):
        pago_pendiente = self.queryset.get(pk=pk)
        movimiento = pago_pendiente.pagar()
        with transaction.atomic():
            if pago_pendiente.pago_unico:
                pago_pendiente.estatus = PagoPendiente.PAGADO
                pago_pendiente.save()
            with open("imageToSave.png", "wb") as fh:
                str_bytes = (request.POST['adjunto'])
                movimiento.adjunto = fh
                movimiento.save()
            movimiento.define_cantidad()
            movimiento.tarjeta.define_balance()
        return Response(status=status.HTTP_200_OK)
