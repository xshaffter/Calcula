from django.conf import settings
from django.core.management.base import BaseCommand

from cat.models import Conversion
import requests


class Command(BaseCommand):
    help = 'Create init data'

    def handle(self, *args, **options):
        conversiones = Conversion.objects.all()
        for conversion in conversiones:
            url = getattr(settings, "CURRENCY_API")
            origen, objetivo = conversion.moneda_origen.nombre_corto.upper(), conversion.moneda_objetivo.nombre_corto.upper()
            api = url.format(origen, objetivo)
            resp = requests.get(api)
            response = resp.json()
            conversion.factor = response['{}_{}'.format(origen, objetivo)]
            conversion.save()
