from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

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


@api_view(['POST'])
def news_create(request):
    news = News(author=request.user)
    serializer = NewsSerializer(news, data=request.data, context={'request':request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def news_update(request, pk):
    try:
        news = News.objects.get(pk=pk)
    except:
        data = {'error':'this news does not exists'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    serializer = NewsSerializer(news, data=request.data, context={'request':request})
    data = {}
    if serializer.is_valid():
        serializer.save()
        data['success'] = 'succesfuly updated'
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def news_delete(request, pk):
    try:
        news = News.objects.get(pk=pk)
    except:
        data = {'error':'this news does not exists'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    operation = news.delete()
    data = {}
    if operation:
        data['success'] = 'successfuly deleted'
    else:
        data['error'] = 'delete failed'
    return Response(data=data)
