from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from contact import serializers

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


@api_view(['POST'])
def contact_create(request):
    contact = Contact(user=request.user)
    serializer = ContactSerializer(contact, data=request.data, context={'request':request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def contact_update(request, pk):
    try:
        contact = Contact.objects.get(pk=pk)
    except:
        data = {'error':'this contact does not exists'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    serializer = ContactSerializer(contact, data=request.data, context={'request':request})
    data = {}
    if serializer.is_valid():
        serializer.save()
        data['success'] = 'successfuly updated'
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def contact_delete(request, pk):
    try:
        contact = Contact.objects.get(pk=pk)
    except:
        data = {'error':'this contact does not exists'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    operation = contact.delete()
    data = {}
    if operation:
        data['success'] = 'successfuly deleted'
    else:
        data['error'] = 'delete failed'
    return Response(data=data)
    