from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render


def main(request):
    return render(request, 'pages/main.html')


def history(request):
    return render(request, 'pages/history.html')


def structure(request):
    return render(request, 'pages/structure.html')


def handler404(request, *args, **kwargs):
    return render(request, '404.html', status=404)
