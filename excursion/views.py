from rest_framework import viewsets, permissions

from .serializers import ExcursionSerializer
from .models import Excursion


class ExcursionViewSet(viewsets.ModelViewSet):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer
    permission_classes = [permissions.IsAuthenticated]
