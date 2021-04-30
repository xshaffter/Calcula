from django.shortcuts import render


def dashboard(request):
    context = {

    }
    return render(request, 'base.html', context)


def close_modal(request):
    return render(request, 'components/close_modal.html')