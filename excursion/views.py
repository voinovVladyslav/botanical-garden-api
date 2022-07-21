from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from excursion.models import Excursion
from excursion.serializers import ExcursionSerializer


@api_view(['GET'])
def excursions(request):
    excursions = Excursion.objects.all()
    serializer = ExcursionSerializer(excursions, many=True, context={'request':request})

    return Response(serializer.data)


@api_view(['GET'])
def excursion_detail(request, pk):
    try:
        excursion = Excursion.objects.get(pk=pk)
    except:
        data = {'error':'this excursion does not exists'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        
    serializer = ExcursionSerializer(excursion, context={'request':request})

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def excursion_create(request):
    excursion = Excursion(user=request.user)
    serializer = ExcursionSerializer(excursion, data=request.data, context={'request':request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def excursion_update(request, pk):
    try:
        excursion = Excursion.objects.get(pk=pk)
    except:
        data = {'error':'this excursion does not exists'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    if request.user != excursion.user:
        return Response({'detail':'access denied'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ExcursionSerializer(excursion, data=request.data, context={'request':request})
    data = {}

    if serializer.is_valid():
        serializer.save()
        data['success'] = 'succesfuly updated'
        return Response(data=data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def excursion_delete(request, pk):
    try:
        excursion = Excursion.objects.get(pk=pk)
    except:
        data = {'error':'this excurion does not exists'}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    if request.user != excursion.user:
        return Response({'detail':'access denied'}, status=status.HTTP_403_FORBIDDEN)

    operation = excursion.delete()
    data = {}
    if operation:
        data['success'] = 'successfuly deleted'
    else:
        data['error'] = 'delete failed'
    return Response(data=data)
