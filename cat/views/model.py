from django.apps import apps

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import path, resolve

from cat import forms


def get_model_or_404(model):
    try:
        model_class = apps.get_model('cat', model.title())
    except LookupError or ValueError:
        raise Http404

    view, args, kwargs = resolve(f'/api/{model}/')
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
        'item': item,
        'id_parent': id_parent,
    }
    context.update(**get_basic_info(child_model_processed))
    return render(request, f'management/models/{child_model}/add.html', context=context)


urls = [
    path('<str:model>/list/', list, name='model_list'),
    path('<str:model>/add/', add, name='model_add'),
    path('<str:model>/<int:id_model>/delete/', delete, name='model_delete'),
    path('<str:model>/<int:id_model>/detail/', detail, name='model_detail'),
    path('<str:parent_model>/<int:id_parent>/add/<str:child_model>/', model_sub_add, name='model_sub_add'),
]
