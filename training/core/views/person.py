from rest_framework.viewsets import ModelViewSet

from training.core.models import Person
from training.core.serializers import PersonListSerializer, PersonSerializer


class PersonViewSet(ModelViewSet):
    # list, retrieve, create, update, partial_update, destroy
    queryset = Person.objects.all()
    per_action_serializer = {"list": PersonListSerializer}

    def get_serializer_class(self):
        serializer = self.per_action_serializer.get(self.action)
        return serializer if serializer is not None else PersonSerializer
