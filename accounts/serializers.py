from django.contrib.auth.models import User, Group
from rest_framework import serializers

from accounts.models import Customer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    customer = serializers.HyperlinkedRelatedField(
        view_name='customer-detail',
        read_only=True
    )
    class Meta:
        model = User
        fields = ['url', 'username', 'groups', 'customer']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
