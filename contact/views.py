from rest_framework import viewsets

from .models import Contact
from .serializers import ContactSerializer
from botanical_garden.permissions import IsAuthorOrIsManagerOrReadOnly


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('-id')
    serializer_class = ContactSerializer
    permission_classes = [IsAuthorOrIsManagerOrReadOnly]
