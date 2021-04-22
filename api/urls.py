from rest_framework import routers

from api.views.common import ModelDataViewSet
from api.views.pago_pendiente import PagoPendienteViewSet
from api.views.tarjeta import TarjetaViewSet
# from api.views.abono_pendiente import AbonoPendiente
from api.views.movimiento import MovimientoViewSet

router = routers.DefaultRouter()

# router.register(r'stat', StatViewSet)
# router.register(r'item', ItemViewSet)
# router.register(r'sprite', SpriteViewSet)
router.register(r'pagopendiente', PagoPendienteViewSet)
router.register(r'tarjeta', TarjetaViewSet)
router.register(r'movimiento', MovimientoViewSet)
router.register(r'modeldata', ModelDataViewSet, basename='modeldata')

url_patterns = router.urls
