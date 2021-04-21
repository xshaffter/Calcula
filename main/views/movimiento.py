from django import views
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from cat.models import Movimiento
from main.forms import MovimientoForm


def adjuntos_movimiento(request, movimiento_id):
    movimiento = get_object_or_404(Movimiento, pk=movimiento_id)
    context = {
        'movimiento': movimiento,
    }
    return render(request, 'management/models/movimiento/adjuntos.html', context)


def detalle_movimiento(request, movimiento_id):
    movimiento = get_object_or_404(Movimiento, pk=movimiento_id)
    form = MovimientoForm(instance=movimiento)
    context = {
        'form': form,
        'movimiento': movimiento,
    }
    return render(request, 'management/models/movimiento/detalle.html', context)


class MovimientoEditView(views.View):
    def get(self, request, movimiento_id):
        movimiento = get_object_or_404(Movimiento, pk=movimiento_id)
        form = MovimientoForm(instance=movimiento)
        context = {
            'form': form,
            'movimiento': movimiento,
        }
        return render(request, 'management/models/movimiento/form.html', context)

    def post(self, request, movimiento_id):
        movimiento = get_object_or_404(Movimiento, pk=movimiento_id)
        form = MovimientoForm(request.POST, request.FILES, instance=movimiento)
        if form.is_valid():
            form.save()
            return redirect('tarjeta_detalle', tarjeta_id=movimiento.tarjeta_id)
        context = {
            'form': form,
            'movimiento': movimiento,
        }
        return render(request, 'management/models/movimiento/form.html', context)


def eliminar_movimiento(request, movimiento_id):
    movimiento = get_object_or_404(Movimiento, pk=movimiento_id)
    tarjeta = movimiento.tarjeta
    tarjeta_id = movimiento.tarjeta_id
    movimiento.delete()
    tarjeta.define_balance()
    return redirect('tarjeta_detalle', tarjeta_id=tarjeta_id)


def actualizar_movimiento(request, movimiento_id):
    next = request.GET.get('next', False)
    movimiento = get_object_or_404(Movimiento, pk=movimiento_id)
    tarjeta = movimiento.tarjeta
    movimiento.define_cantidad()
    tarjeta.define_balance()
    if not next:
        return redirect('tarjeta_detalle', movimiento.tarjeta_id)
    else:
        return HttpResponseRedirect(next)