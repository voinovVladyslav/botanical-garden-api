from rest_framework import serializers

from news.models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'hashtag']
        read_only_fieds = ['id']

class NewsDetailSerializer(NewsSerializer):
    class Meta(NewsSerializer.Meta):
        fields = NewsSerializer.Meta.fields + ['context', 'publication_date']
        read_only_fieds = NewsSerializer.Meta.read_only_fieds + ['publication_date']
