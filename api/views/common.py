from django.apps import apps
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.serializers import ModelDataSerializer


class ModelDataViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        module = request.GET.get('module', False)
        if module:
            model = apps.get_model('cat', module)
            if model:
                data = {
                    'headers': model.TABLE_HEADERS
                }
                serializer = ModelDataSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                return Response(data=serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
