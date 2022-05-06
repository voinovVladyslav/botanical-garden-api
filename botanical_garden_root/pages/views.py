from django.shortcuts import render


def main(request):
    return render(request, 'pages/main.html')


def history(request):
    return render(request, 'pages/history.html')


def structure(request):
    return render(request, 'pages/structure.html')
