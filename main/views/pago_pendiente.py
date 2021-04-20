from django import views
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from cat.models import PagoPendiente, Tarjeta
from main.forms import PagoPendienteForm


def pago_pendiente_detalle(request, pago_pendiente_id):
    pago_pendiente = get_object_or_404(PagoPendiente, pk=pago_pendiente_id)
    form = PagoPendienteForm(instance=pago_pendiente)
    context = {
        'form': form,
        'pago_pendiente': pago_pendiente,
    }
    return render(request, 'pago_pendiente/detalle.html', context)


class PagoPendienteEditView(views.View):

    def get(self, request, pago_pendiente_id):
        pago_pendiente = get_object_or_404(PagoPendiente, pk=pago_pendiente_id)
        form = PagoPendienteForm(instance=pago_pendiente)
        context = {
            'form': form,
            'pago_pendiente': pago_pendiente,
        }
        return render(request, 'pago_pendiente/form.html', context)

    def post(self, request, pago_pendiente_id):
        pago_pendiente = get_object_or_404(PagoPendiente, pk=pago_pendiente_id)
        form = PagoPendienteForm(instance=pago_pendiente, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tarjeta_detalle', tarjeta_id=pago_pendiente.tarjeta_id)
        context = {
            'form': form,
            'pago_pendiente': pago_pendiente,
        }
        return render(request, 'pago_pendiente/form.html', context)


class PagoPendienteCreateView(views.View):

    def get(self, request, tarjeta_id):
        tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
        form = PagoPendienteForm()
        context = {
            'form': form,
            'tarjeta': tarjeta,
        }
        return render(request, 'pago_pendiente/form.html', context)

    def post(self, request, tarjeta_id):
        tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
        form = PagoPendienteForm(data=request.POST)
        if form.is_valid():
            pago_pendiente = form.save(commit=False)
            pago_pendiente.tarjeta = tarjeta
            pago_pendiente.save()
            return redirect('tarjeta_detalle', tarjeta_id=tarjeta_id)
        context = {
            'form': form,
            'tarjeta': tarjeta,
        }
        return render(request, 'pago_pendiente/form.html', context)


def eliminar_pago_pendiente(request, pago_pendiente_id):
    pago_pendiente = get_object_or_404(PagoPendiente, pk=pago_pendiente_id)
    tarjeta_id = pago_pendiente.tarjeta_id
    pago_pendiente.delete()
    return redirect('tarjeta_detalle', tarjeta_id=tarjeta_id)


def pago_pendiente_pagar(request, pago_pendiente_id):
    next = request.GET.get('next', False)
    pago_pendiente = get_object_or_404(PagoPendiente, pk=pago_pendiente_id)

    movimiento = pago_pendiente.pagar()
    with transaction.atomic():
        if pago_pendiente.pago_unico:
            pago_pendiente.estatus = PagoPendiente.PAGADO
            pago_pendiente.save()
        movimiento.adjunto = request.FILES['adjunto']
        movimiento.save()
        movimiento.define_cantidad()
        movimiento.tarjeta.define_balance()
    if not next:
        return redirect('tarjeta_detalle', pago_pendiente.tarjeta_id)
    else:
        return HttpResponseRedirect(next)
