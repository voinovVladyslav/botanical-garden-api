from rest_framework import serializers

from excursion.models import Excursion


class ExcursionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excursion
        fields = ['id', 'type', 'date']
        read_only_fields = ['id']
        extra_kwargs = {'type': {'required': True}}

