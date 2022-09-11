from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from news.models import News, Hashtag
from news.serializers import (
    NewsSerializer,
    NewsDetailSerializer,
    NewsImageSerializer,
    HashtagSerializer,
)
from news.permissions import IsManagerOrReadOnly


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'hashtags',
                OpenApiTypes.STR,
                description='List of hashtags id to filter',
            ),
            OpenApiParameter(
                'publication_date_lte',
                OpenApiTypes.STR,
                description='Lower than equal date',
            ),
            OpenApiParameter(
                'publication_date_gte',
                OpenApiTypes.STR,
                description='Greater than equal date',
            ),
        ]
    )
)
class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    permission_classes = [IsManagerOrReadOnly]
    authentication_classes = [TokenAuthentication]
    serializer_class = NewsDetailSerializer

    def _params_to_int(self, qs):
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        hashtags = self.request.query_params.get('hashtags')
        publication_date_gte = self.request.query_params.get('publication_date_gte')
        publication_date_lte = self.request.query_params.get('publication_date_lte')
        queryset = self.queryset

        if hashtags:
            hashtag_ids = self._params_to_int(hashtags)
            queryset = queryset.filter(hashtags__id__in=hashtag_ids)
        if publication_date_gte:
            queryset = queryset.filter(publication_date__gte=publication_date_gte)
        if publication_date_lte:
            queryset = queryset.filter(publication_date__lte=publication_date_lte)

        return queryset.order_by('-id').distinct()

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


class HashtagViewSet(ModelViewSet):
    queryset = Hashtag.objects.all()
    permission_classes = [IsManagerOrReadOnly]
    authentication_classes = [TokenAuthentication]
    serializer_class = HashtagSerializer

    def get_queryset(self):
        return self.queryset.order_by('-name')
