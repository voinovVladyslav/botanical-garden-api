from django.shortcuts import redirect, render

from excursion.forms import ExcursionForm
from news.models import News

def main(request):
    news = News.objects.all().order_by('-id')[:2]
    first_news = news[0]
    second_news = news[1]

    if request.method == "POST":
        form = ExcursionForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.person = request.user.customer
            t.save()
            return redirect('profile')
    else:
        form = ExcursionForm()

    context = {'form': form, 'first_news': first_news, 'second_news': second_news}
    return render(request, 'pages/main.html', context)


def history(request):
    return render(request, 'pages/history.html')


def structure(request):
    return render(request, 'pages/structure.html')
