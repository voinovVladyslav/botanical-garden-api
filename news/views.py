from rest_framework import viewsets

from .models import News
from .serializers import NewsSerializer
from botanical_garden.permissions import IsManagerOrReadOnly


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer
    permission_classes = [IsManagerOrReadOnly]
