import json

from rest_framework import viewsets, status
from rest_framework.response import Response

from api.serializers import MovimientoSerializer
from cat.models import Movimiento


class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer

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