from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from cat.models import AbonoPendiente


class AbonoPendienteViewSet(viewsets.ModelViewSet):
    queryset = AbonoPendiente.objects.all()
    serializer_class = AbonoPendienteSerializer

    @action(detail=True, methods=['get', 'post'])
    def delete(self, request, pk=None):
        instance = get_object_or_404(AbonoPendiente, pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)
