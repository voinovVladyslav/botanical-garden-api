from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication

from news.models import News
from news.serializers import (
    NewsSerializer,
    NewsDetailSerializer,
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
        return self.serializer_class
