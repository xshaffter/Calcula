from django import views
from django.apps import apps

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.urls import path, resolve

from cat import forms
from cat.models import Tarjeta


def get_model_or_404(model):
    try:
        model_class = apps.get_model('cat', model.title())
        view, args, kwargs = resolve(f'/api/{model}/')
    except LookupError or ValueError:
        raise Http404
    return model_class


def get_basic_info(model):
    model_class = apps.get_model('cat', model.title())
    return {
        'main_url': f"/cat/{model}/",
        'end_point': f"/api/{model}/",
        'module': model_class._meta.verbose_name,
        'module_plural': model_class._meta.verbose_name_plural
    }


def list(request, model):
    model_class = get_model_or_404(model)
    context = {
        'model': model

    }
    context.update(**get_basic_info(model))
    return render(request, 'components/list.html', context=context)


def add(request, model):
    model_class = get_model_or_404(model)
    form_class = getattr(forms, f'{model.capitalize()}Form')
    form = form_class()
    context = {
        'form': form,
    }
    context.update(**get_basic_info(model))
    return render(request, f'management/models/{model}/add.html', context=context)


class DeleteView(views.View):
    def get(self, request, model, id_model):
        model_class = get_model_or_404(model)
        item = get_object_or_404(model_class, pk=id_model)
        context = {
            'item': item,
            'action': 'Eliminar',
            'module': model,
        }
        return render(request, f'management/models/{model}/delete.html', context=context)

    def post(self, request, model, id_model):
        model_class = get_model_or_404(model)
        instance = get_object_or_404(model_class, pk=id_model)
        tarjeta = instance.tarjeta  # type: Tarjeta
        instance.delete()
        tarjeta.define_balance()
        return redirect('app:close_modal')


def detail(request, model, id_model):
    model_class = get_model_or_404(model)
    form_class = getattr(forms, f'{model.capitalize()}Form')
    item = get_object_or_404(model_class, pk=id_model)
    form = form_class()
    context = {
        'form': form,
        'item_id': id_model,
        'item': item
    }
    context.update(**get_basic_info(model))
    return render(request, f'management/models/{model}/detail.html', context=context)


def model_sub_add(request, parent_model, id_parent, child_model):
    child_model_processed = child_model.replace("_", " ").title().replace(" ", "")
    parent_model_processed = parent_model.replace("_", " ").title().replace(" ", "")
    parent_model_class = get_model_or_404(parent_model_processed)
    child_model_class = get_model_or_404(child_model_processed)
    form_class = getattr(forms, f'{child_model_processed}Form')
    item = get_object_or_404(parent_model_class, pk=id_parent)
    form = form_class()
    context = {
        'parent_model': parent_model_processed.lower(),
        'child_model': child_model_processed.lower(),
        'form': form,
        'parent': item,
        'id_parent': id_parent,
    }
    context.update(**get_basic_info(child_model_processed))
    return render(request, f'management/models/{child_model}/add.html', context=context)


class PerformActionView(views.View):
    def get(self, request, model, id_model, action):
        model_class = get_model_or_404(model)
        form_class = getattr(forms, f'{model.capitalize()}{action.capitalize()}Form')
        item = get_object_or_404(model_class, pk=id_model)
        form = form_class(instancia=item)
        context = {
            'form': form,
            'item_id': id_model,
            'item': item,
            'action': action,
            'model': model,
        }
        context.update(**get_basic_info(model))
        return render(request, f'management/models/{model}/{action}.html', context=context)

    def post(self, request, model, id_model, action):
        model_class = get_model_or_404(model)
        form_class = getattr(forms, f'{model.capitalize()}{action.capitalize()}Form')
        item = get_object_or_404(model_class, pk=id_model)
        form = form_class(item, request.POST, request.FILES)
        if form.is_valid():
            form.save()
        context = {
            'form': form,
            'item_id': id_model,
            'item': item,
            'action': action,
            'model': model,
        }
        context.update(**get_basic_info(model))
        return redirect('app:close_modal')


urls = [
    path('<str:model>/list/', list, name='model_list'),
    path('<str:model>/add/', add, name='model_add'),
    path('<str:model>/<int:id_model>/delete/', DeleteView.as_view(), name='model_delete'),
    path('<str:model>/<int:id_model>/detail/', detail, name='model_detail'),
    path('<str:model>/<int:id_model>/<str:action>/', PerformActionView.as_view(), name='model_perform_action'),
    path('<str:parent_model>/<int:id_parent>/add/<str:child_model>/', model_sub_add, name='model_sub_add'),
]
