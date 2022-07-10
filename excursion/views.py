from rest_framework import viewsets, permissions
from rest_framework import generics

from .serializers import ExcursionSerializer
from .models import Excursion


class ExcursionViewSet(viewsets.ModelViewSet):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExcursionList(generics.ListAPIView):
    serializer_class = ExcursionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Excursion.objects.filter(user=user)
