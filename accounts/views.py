from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group

from accounts.models import Customer
from accounts.serializers import * 


@api_view(['GET'])
def users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True, context={'request':request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAdminUser])
def customers(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True, context={'request':request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except:
        data = {'error':'this customer does not exist'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    if request.user != customer.user:
        return Response({'detail':'access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CustomerSerializer(customer, context={'request':request})
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def customer_update(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except:
        data = {'error':'this customer does not exist'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    if request.user != customer.user:
        return Response({'detail':'access denied'}, status=status.HTTP_403_FORBIDDEN)

    data = {}
    serializer = CustomerSerializer(customer, data=request.data)  

    if serializer.is_valid():
        serializer.save()
        data['success'] = 'successfuly updated'
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def registration(request):
    serializer = RegistrationSerializer(data=request.data) 
    data = {}

    if serializer.is_valid():
        user = serializer.save()
        data['response'] = 'successfully registered a new user'
        data['username'] = user.username
        data['email'] = user.email 
        token = Token.objects.get(user=user).key
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)
        