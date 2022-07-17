from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from news.models import News
from news.serializers import NewsSerializer


@api_view(['GET'])
def news(request):
    news = News.objects.all()
    serializer = NewsSerializer(news, many=True, context={'request':request})

    return Response(serializer.data)


@api_view(['GET'])
def news_detail(request, pk):
    try:
        news = News.objects.get(pk=pk)
    except:
        data = {'error':'this news does not exists'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        
    serializer = NewsSerializer(news, context={'request':request})

    return Response(serializer.data)
