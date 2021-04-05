from rest_framework.viewsets import ModelViewSet

from training.core.models import Person
from training.core.serializers import PersonModelSerializer, PersonReadOnlySerializer


class PersonViewSet(ModelViewSet):
    """
    GET /person -> list
    GET /person/id -> retrieve
    POST /person -> create
    PUT /person/id -> update
    PATCH /person/id -> partial_update
    DELETE /person/id -> destroy
    """

    queryset = Person.objects.all()
    per_action_serializer = {"list": PersonReadOnlySerializer}

    def get_serializer_class(self):
        serializer = self.per_action_serializer.get(self.action)
        return serializer if serializer is not None else PersonModelSerializer
