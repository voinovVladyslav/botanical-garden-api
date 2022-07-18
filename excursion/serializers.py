from rest_framework import serializers

from .models import Excursion


class ExcursionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='excursion_detail',
        lookup_field='pk',
    )

    user = serializers.HyperlinkedRelatedField(
        view_name='user_detail',
        lookup_field='pk',
        read_only=True,
    )

    class Meta:
        model = Excursion
        fields = '__all__'
