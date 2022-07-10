from rest_framework import viewsets, permissions

from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('-id')
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
