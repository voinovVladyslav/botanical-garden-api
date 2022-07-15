from rest_framework import viewsets 
from rest_framework import generics

from .serializers import ExcursionSerializer
from .models import Excursion
from botanical_garden.permissions import IsAuthorOrReadOnly


class ExcursionViewSet(viewsets.ModelViewSet):
    queryset = Excursion.objects.all().order_by('date', 'time')
    serializer_class = ExcursionSerializer
    permission_classes = [IsAuthorOrReadOnly]

class ExcursionList(generics.ListAPIView):
    serializer_class = ExcursionSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Excursion.objects.filter(user=user)
