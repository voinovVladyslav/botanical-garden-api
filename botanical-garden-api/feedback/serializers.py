from rest_framework import serializers

from feedback.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','rating', 'description',]
        read_only_fields = ['id']
