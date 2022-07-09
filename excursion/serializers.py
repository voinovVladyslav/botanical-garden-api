from rest_framework import serializers

from .models import Excursion


class ExcursionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Excursion
        fields = '__all__'
