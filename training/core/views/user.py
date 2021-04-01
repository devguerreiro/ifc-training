from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListAPIView

from training.core.models import CustomUser
from training.core.serializers import UserListSerializer


class UserViewSet(GenericViewSet, ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
