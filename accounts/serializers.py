from django.contrib.auth.models import User, Group
from rest_framework import serializers

from accounts.models import Customer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name = 'user_detail',
        lookup_field = 'pk',
    )
    '''
    customer = serializers.HyperlinkedRelatedField(
        view_name='customer-detail',
        read_only=True
    )
    '''

    class Meta:
        model = User
        fields = ['url', 'username', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name = 'customer_detail',
        lookup_field = 'pk',
    )
    user = serializers.HyperlinkedRelatedField(
        view_name = 'user_detail',
        lookup_field = 'pk',
        read_only = True,
    )
    
    class Meta:
        model = Customer
        fields = '__all__'
