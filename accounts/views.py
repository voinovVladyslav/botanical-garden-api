from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from .serializers import *
from botanical_garden.permissions import IsAuthorOrReadOnly, OnlySelf, ReadOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [OnlySelf]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [ReadOnly]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-user')
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthorOrReadOnly]
