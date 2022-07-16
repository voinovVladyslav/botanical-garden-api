from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from accounts import serializers

from accounts.models import Customer
from accounts.serializers import CustomerSerializer, UserSerializer, GroupSerializer


@api_view(['GET'])
def users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True, context={'request':request})
    return Response(serializer.data)


@api_view(['GET'])
def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    serializer = UserSerializer(user, context={'request':request})
    return Response(serializer.data)


@api_view(['GET'])
def customers(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True, context={'request':request})
    return Response(serializer.data)


@api_view(['GET'])
def customer_detail(request, pk):
    customer = Customer.objects.get(pk=pk)
    serializer = CustomerSerializer(customer, context={'request':request})
    return Response(serializer.data)
