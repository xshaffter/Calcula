import json

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.paginators import ShortResultsSetPagination
from api.serializers import AbonoPendienteSerializer
from cat.models import AbonoPendiente


class AbonoPendienteViewSet(viewsets.ModelViewSet):
    queryset = AbonoPendiente.objects.all()
    serializer_class = AbonoPendienteSerializer
    pagination_class = ShortResultsSetPagination

    def list(self, request, *args, **kwargs):
        tarjeta = request.GET.get('parent_id')
        queryset = self.queryset.filter(tarjeta_id=tarjeta).exclude(estatus=AbonoPendiente.PAGADO)
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

    @action(detail=True, methods=['get', 'post'])
    def delete(self, request, pk=None):
        instance = get_object_or_404(AbonoPendiente, pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)
