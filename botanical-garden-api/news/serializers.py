from rest_framework import serializers

from news.models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'hashtag']
        read_only_fieds = ['id']

class NewsDetailSerializer(NewsSerializer):
    class Meta(NewsSerializer.Meta):
        fields = NewsSerializer.Meta.fields + ['context', 'publication_date', 'image']
        read_only_fieds = NewsSerializer.Meta.read_only_fieds + ['publication_date']


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': True}}
