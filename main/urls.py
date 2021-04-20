from django.urls import path

from main.views import tarjeta as tarjeta_views, main as main_views, movimiento as movimiento_views, pago_pendiente as pago_pendiente_views

urlpatterns = [
    path('tarjeta/list/', tarjeta_views.TarjetaListView.as_view(), name="tarjeta_list"),
    path('tarjeta/<int:tarjeta_id>/actualizar/', tarjeta_views.refresh_tarjeta, name="tarjeta_refresh"),
    path('tarjeta/<int:tarjeta_id>/movimiento/add/', tarjeta_views.MovimientoFormView.as_view(), name="tarjeta_add_movimiento"),
    path('tarjeta/<int:tarjeta_id>/detalle/', tarjeta_views.detalle_tarjeta, name="tarjeta_detalle"),

    path('movimiento/<int:movimiento_id>/adjuntos/', movimiento_views.adjuntos_movimiento, name="movimiento_adjuntos"),
    path('movimiento/<int:movimiento_id>/edit/', movimiento_views.MovimientoEditView.as_view(), name="movimiento_edit"),
    path('movimiento/<int:movimiento_id>/detalle/', movimiento_views.detalle_movimiento, name="movimiento_detalle"),
    path('movimiento/<int:movimiento_id>/eliminar/', movimiento_views.eliminar_movimiento, name="movimiento_eliminar"),
    path('movimiento/<int:movimiento_id>/actualizar/', movimiento_views.actualizar_movimiento, name="movimiento_refresh"),

    path('tarjeta/<int:tarjeta_id>/pago_pendiente/add/', pago_pendiente_views.PagoPendienteCreateView.as_view(), name="tarjeta_add_pago_pendiente"),
    path('pago_pendiente/<int:pago_pendiente_id>/detalle/', pago_pendiente_views.pago_pendiente_detalle, name="pago_pendiente_detalle"),
    path('pago_pendiente/<int:pago_pendiente_id>/editar/', pago_pendiente_views.PagoPendienteEditView.as_view(), name="pago_pendiente_editar"),
    path('pago_pendiente/<int:pago_pendiente_id>/pagar/', pago_pendiente_views.pago_pendiente_pagar, name="pago_pendiente_pagar"),
    path('pago_pendiente/<int:pago_pendiente_id>/eliminar/', pago_pendiente_views.eliminar_pago_pendiente, name="pago_pendiente_eliminar"),
    path('', main_views.dashboard, name="dashboard"),
]
