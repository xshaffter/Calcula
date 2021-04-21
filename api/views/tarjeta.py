import json

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import TarjetaSerializer
from cat.models import Tarjeta


class TarjetaViewSet(viewsets.ModelViewSet):
    queryset = Tarjeta.objects.all()
    serializer_class = TarjetaSerializer

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

    @action(detail=True, methods=['get'])
    def refresh(self, request, pk=None, *args, **kwargs):
        instance = self.queryset.get(pk=pk)
        instance.define_balance()
        return Response(status=status.HTTP_200_OK)