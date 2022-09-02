from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from news.models import News
from news.serializers import (
    NewsSerializer,
    NewsDetailSerializer,
    NewsImageSerializer,
)
from news.permissions import IsManagerOrReadOnly


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    permission_classes = [IsManagerOrReadOnly]
    authentication_classes = [TokenAuthentication]
    serializer_class = NewsDetailSerializer

    def get_queryset(self):
        return self.queryset.order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsSerializer
        elif self.action == 'upload_image':
            return NewsImageSerializer
        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        news = self.get_object()
        serializer = self.get_serializer(news, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
