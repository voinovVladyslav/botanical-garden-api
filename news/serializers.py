from rest_framework import serializers

from .models import News


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='news_detail',
        lookup_field='pk'
    )
    author = serializers.HyperlinkedRelatedField(
        view_name='user_detail',
        lookup_field='pk',
        read_only=True,
    )

    class Meta:
        model = News
        fields = '__all__'