from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='contact_detail',
        lookup_field='pk',
    )

    user = serializers.HyperlinkedRelatedField(
        view_name='user_detail',
        lookup_field='pk',
        read_only=True,
    )

    class Meta:
        model = Contact
        fields = '__all__'
