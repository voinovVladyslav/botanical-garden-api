from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from excursion.models import Excursion


class ExcursionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excursion
        fields = ['id', 'type', 'date']
        read_only_fields = ['id']
