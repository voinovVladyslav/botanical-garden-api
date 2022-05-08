from django.shortcuts import render, redirect
from .models import News
from .forms import CreateNews
from .decorators import allowed_users

# Create your views here.

def news_all(request):
    news = News.objects.all().order_by('-id')

    context = {'news': news}
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