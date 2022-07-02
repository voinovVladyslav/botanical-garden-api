from django.shortcuts import redirect, render

from excursion.forms import ExcursionForm
from news.models import News

def main(request):
    news = News.objects.all().order_by('-id')[:2]
    try:
        first_news, second_news = news[0], news[1]
    except:
        first_news, second_news = None, None
    form = ExcursionForm()
    
    if request.method == "POST":
        form = ExcursionForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.person = request.user
            t.save()
            return redirect('excursions')

    context = {'form': form, 'first_news': first_news, 'second_news': second_news}
    return render(request, 'pages/main.html', context)


def history(request):
    return render(request, 'pages/history.html')


def structure(request):
    return render(request, 'pages/structure.html')
