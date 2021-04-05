from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet

from training.core.models import CustomUser
from training.core.serializers import UserReadOnlySerializer


class UserViewSet(GenericViewSet, ListAPIView):
    """
    GET /person -> list
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserReadOnlySerializer
