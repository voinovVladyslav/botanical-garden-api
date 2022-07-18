from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

from contact.models import Contact
from contact.serializers import ContactSerializer


@api_view(['GET'])
def contacts(request):
    contacts = Contact.objects.all()
    serializer = ContactSerializer(contacts, many=True, context={'request':request})

    return Response(serializer.data)


@api_view(['GET'])
def contact_detail(request, pk):
    try:
        contact = Contact.objects.get(pk=pk)
    except:
        data = {'error':'this contact does not exists'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ContactSerializer(contact, context={'request':request})
    return Response(serializer.data)
