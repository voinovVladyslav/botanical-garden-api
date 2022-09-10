from rest_framework import serializers

from news.models import News, Hashtag


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name']
        read_only_fields = ['id']


class NewsSerializer(serializers.ModelSerializer):
    hashtags = HashtagSerializer(many=True, required=False)
    class Meta:
        model = News
        fields = ['id', 'title', 'hashtags']
        read_only_fieds = ['id']

    def create(self, validated_data):
        hashtags = validated_data.pop('tags', [])
        news = News.objects.create(**validated_data)
        for hashtag in hashtags:
            hashtag_obj, created = Hashtag.objects.get_or_create(
                **hashtag
            )
            news.hashtags.add(hashtag_obj)

        return news

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


