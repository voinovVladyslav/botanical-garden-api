from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from excursion.models import Excursion
from excursion.serializers import ExcursionSerializer


class ExcursionViewSet(ModelViewSet):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
