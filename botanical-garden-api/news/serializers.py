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

    def _get_or_create_hashtags(self, hashtags, news):
        for hashtag in hashtags:
            hashtag_obj, created = Hashtag.objects.get_or_create(**hashtag)
            news.hashtags.add(hashtag_obj)


    def create(self, validated_data):
        hashtags = validated_data.pop('hashtags', [])
        news = News.objects.create(**validated_data)
        self._get_or_create_hashtags(hashtags, news)
        return news

    def update(self, instance, validated_data):
        hashtags = validated_data.pop('hashtags', None)
        if hashtags is not None:
            instance.hashtags.clear()
            self._get_or_create_hashtags(hashtags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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


