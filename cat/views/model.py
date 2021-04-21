from django.apps import apps

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import path, resolve

from cat import forms


def get_model_or_404(model):
    try:
        model_class = apps.get_model('cat', model.capitalize())
    except LookupError or ValueError:
        raise Http404

    view, args, kwargs = resolve(f'/api/{model}/')
    return model_class


def get_basic_info(model):
    model_class = apps.get_model('cat', model.capitalize())
    return {
        'main_url': f"/cat/{model}/",
        'end_point': f"/api/{model}/",
        'module': model_class._meta.verbose_name,
        'module_plural': model_class._meta.verbose_name_plural
    }


def list(request, model):
    model_class = get_model_or_404(model)
    context = {
        'weapons': model_class.objects.all()
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


def delete(request, model, id_model):
    model_class = get_model_or_404(model)
    instance = get_object_or_404(model_class, pk=id_model)
    instance.delete()
    return HttpResponseRedirect(reverse('cat:model_list', kwargs={'model': model}))


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


urls = [
    path('<str:model>/list/', list, name='model_list'),
    path('<str:model>/add/', add, name='model_add'),
    path('<str:model>/<int:id_model>/delete/', delete, name='model_delete'),
    path('<str:model>/<int:id_model>/detail/', detail, name='model_detail'),
]
