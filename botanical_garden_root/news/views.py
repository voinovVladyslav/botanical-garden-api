from django.shortcuts import render
from .models import News
from .forms import CreateNews

# Create your views here.
def news_all(request):
    news = News.objects.all()

    context = {'news': news}
    return render(request, 'news/news.html', context=context)

def news_single(request, news_pk):
    news = News.objects.get(id=news_pk)
    
    context = {'news': news}
    return render(request, 'news/news_single.html', context=context)

def create_news(request):

    if request.method == 'POST':
        form = CreateNews(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CreateNews()

    context = {'form': form}
    return render(request, 'news/create_news.html', context=context)