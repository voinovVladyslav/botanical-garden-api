from django.contrib.auth.models import User, Group
from rest_framework import serializers

from accounts.models import Customer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='user_detail',
        lookup_field='pk',
    )
    customer = serializers.HyperlinkedRelatedField(
        view_name='customer_detail',
        lookup_field='pk',
        read_only=True,
    )
    groups = serializers.HyperlinkedRelatedField(
        view_name='group_detail',
        lookup_field='pk',
        many=True,
        read_only = True,
    )

    class Meta:
        model = User
        fields = ['url', 'username', 'groups', 'customer']


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        user = User(
            username = self.validated_data['username'],
            email = self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'passwords did not match'})

        user.set_password(password)
        user.save()

        Customer.objects.create(email=self.validated_data['email'], user=user)

        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='group_detail',
        lookup_field='pk',
    )

    class Meta:
        model = Group
        fields = ['url', 'name']


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='customer_detail',
        lookup_field='pk',
    )
    user = serializers.HyperlinkedRelatedField(
        view_name='user_detail',
        lookup_field='pk',
        read_only=True,
    )
    
    class Meta:
        model = Customer
        fields = '__all__'
