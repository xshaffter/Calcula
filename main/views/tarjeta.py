from django import views
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from cat.models import Tarjeta
from main.forms import MovimientoForm


class TarjetaListView(views.View):
    def get(self, request):
        context = {

        }
        return render(request, 'tarjeta/list.html', context)


def refresh_tarjeta(request, tarjeta_id):
    next = request.GET.get('next', False)
    tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
    tarjeta.define_balance()
    if not next:
        return redirect('tarjeta_list')
    else:
        return HttpResponseRedirect(next)


class MovimientoFormView(views.View):
    template = 'movimiento/form.html'

    def get(self, request, tarjeta_id):
        tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
        form = MovimientoForm()
        context = {
            'form': form,
            'tarjeta': tarjeta,
        }
        return render(request, self.template, context)

    def post(self, request, tarjeta_id):
        tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
        form = MovimientoForm(request.POST, request.FILES)

        if form.is_valid():
            movimiento = form.save(commit=False)  # type: Movimiento
            movimiento.tarjeta = tarjeta
            movimiento.define_cantidad()
            tarjeta.define_balance()
            return redirect('tarjeta_detalle', tarjeta_id=tarjeta_id)

        context = {
            'form': form,
            'tarjeta': tarjeta,
        }
        return render(request, self.template, context)


def detalle_tarjeta(request, tarjeta_id):
    tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
    movimientos = tarjeta.movimiento_set.all().order_by('-fecha')
    paginator = Paginator(movimientos, 5)
    page = request.GET.get('page', 1)
    try:
        movimientos = paginator.page(page)
    except EmptyPage:
        movimientos = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        movimientos = paginator.page(1)
    context = {
        'tarjeta': tarjeta,
        'movimientos': movimientos
    }
    return render(request, 'tarjeta/detalle.html', context)
