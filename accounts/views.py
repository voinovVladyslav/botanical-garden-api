from rest_framework import status
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
    try:
        user = User.objects.get(pk=pk)
    except:
        data = {'error':'this user does not exists'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, context={'request':request})
    return Response(serializer.data)


@api_view(['GET'])
def groups(request):
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True, context={'request':request})
    return Response(serializer.data)


@api_view(['GET'])
def group_detail(request, pk):
    try:
        group = Group.objects.get(pk=pk)
    except:
        data = {'error':'this group does not exists'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    serializer = GroupSerializer(group, context={'request':request})
    return Response(serializer.data)


@api_view(['GET'])
def customers(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True, context={'request':request})
    return Response(serializer.data)


@api_view(['GET'])
def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except:
        data = {'error':'this customer does not exist'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CustomerSerializer(customer, context={'request':request})
    return Response(serializer.data)
