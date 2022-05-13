from django.shortcuts import render, redirect
from .models import News
from .forms import CreateNews
from botanical_garden.decorators import allowed_users, allowed_users_pk

# Create your views here.

def news_all(request):
    news = News.objects.all().order_by('-id')
    firstnews = News.objects.all().order_by('-id')[:1]

    context = {'news': news, 'firstnews': firstnews}
    return render(request, 'news/news.html', context=context)


def news_single(request, news_pk):
    news = News.objects.get(id=news_pk)
    
    context = {'news': news}
    return render(request, 'news/news_single.html', context=context)


@allowed_users(allowed_roles=['manager', 'admin'])
def create_news(request):

    if request.method == 'POST':
        form = CreateNews(request.POST, request.FILES)
        if form.is_valid():
            t = form.save(commit=False)
            t.author = request.user
            t.save()
            return redirect('news_all')
    else:
        form = CreateNews()

    context = {'form': form}
    return render(request, 'news/create_news.html', context=context)


@allowed_users_pk(allowed_roles=['manager', 'admin'])
def update_news(request, news_pk):
    news = News.objects.get(id=news_pk)
    
    form = CreateNews(request.FILES, instance=news)
    if request.method == 'POST':
        form = CreateNews(request.POST, request.FILES, instance=news)
        if form.is_valid():
            t = form.save(commit=False)
            t.author = request.user
            t.save()
            return redirect('news_all')
    
    context = {'form': form}
    return render(request, 'news/create_news.html', context=context)