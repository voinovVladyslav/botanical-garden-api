from django.http import Http404
from django.shortcuts import render, redirect
from .models import News
from .forms import CreateNews
from botanical_garden.decorators import allowed_users, allowed_users_pk

# Create your views here.

def news_all(request):
    news = News.objects.all().order_by('-id')
    firstnews = News.objects.all().order_by('-id')[:1]
    
    if request.user.groups.filter(name='manager').exists():
        ismanager = True
    else:
        ismanager = False

    context = {'news': news, 'firstnews': firstnews, 'ismanager':ismanager}
    return render(request, 'news/news.html', context=context)


def news_single(request, news_pk):
    news = News.objects.get(id=news_pk)
    
    context = {'news': news}
    return render(request, 'news/news_single.html', context=context)


@allowed_users(allowed_roles=['manager'])
def create_news(request):
    form = CreateNews()
    context = {'form': form}
    return render(request, 'news/create_news.html', context=context)


@allowed_users(allowed_roles=['manager'])
def create_news_only(request):
    if request.method == 'POST':
        form = CreateNews(request.POST, request.FILES)
        if form.is_valid():
            t = form.save(commit=False)
            t.author = request.user
            t.save()
            return redirect('news_all')
    raise Http404()


@allowed_users_pk(allowed_roles=['manager'])
def update_news(request, news_pk):
    news = News.objects.get(id=news_pk)
    form = CreateNews(instance=news)
    
    context = {'form': form, 'news':news}
    return render(request, 'news/update_news.html', context=context)


@allowed_users_pk(allowed_roles=['manager'])
def update_news_only(request, news_pk):
    news = News.objects.get(id=news_pk)
    if request.method == 'POST':
        form = CreateNews(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_all')
    raise Http404()


@allowed_users_pk(allowed_roles=['manager'])
def delete_news(request, news_pk):
    news = News.objects.get(id=news_pk)

    context = {'news': news}
    return render(request, 'news/delete_news.html', context)


@allowed_users_pk(allowed_roles=['manager'])
def delete_news_only(request, news_pk):
    news = News.objects.get(id=news_pk)
    if request.method == 'POST':
        news.delete()
        return redirect('news_all')
    raise Http404()
