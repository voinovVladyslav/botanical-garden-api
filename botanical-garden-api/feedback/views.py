from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from feedback.models import Review
from feedback.serializers import ReviewSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewGlobalViewSet(ReadOnlyModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_queryset(self):
        return self.queryset.order_by('-id')
