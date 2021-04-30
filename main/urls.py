from django.urls import path

from main.views import tarjeta as tarjeta_views, main as main_views, movimiento as movimiento_views, pago_pendiente as pago_pendiente_views

urlpatterns = [
    path('modal/close/', main_views.close_modal, name="close_modal"),
    path('', main_views.dashboard, name="dashboard"),
]
