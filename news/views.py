from rest_framework.decorators import api_view
from rest_framework.response import Response

from news.models import News
from news.serializers import NewsSerializer


@api_view(['GET'])
def get_all_news(request):
    news = News.objects.all()
    serializer = NewsSerializer(news, many=True)

    return Response(serializer.data)
