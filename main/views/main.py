from django.shortcuts import render


def dashboard(request):
    context = {

    }
    return render(request, 'base.html', context)