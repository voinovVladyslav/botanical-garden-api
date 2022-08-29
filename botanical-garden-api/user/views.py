from rest_framework import generics
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken

from user import serializers


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class AuthTokenView(ObtainAuthToken):
    serializer_class = serializers.TokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
