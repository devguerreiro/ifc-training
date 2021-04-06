from rest_framework.viewsets import ModelViewSet

from training.core.models import Person
from training.core.serializers import (
    PersonCreateModelSerializer,
    PersonListSerializer,
    PersonRetrieveSerializer,
    PersonUpdateModelSerializer,
)


class PersonModelViewSet(ModelViewSet):
    """
    GET /person -> list
    GET /person/id -> retrieve
    POST /person -> create
    PUT /person/id -> update
    PATCH /person/id -> partial_update
    DELETE /person/id -> destroy
    """

    queryset = Person.objects.all()
    per_action_serializer = {
        "list": PersonListSerializer,
        "retrieve": PersonRetrieveSerializer,
        "create": PersonCreateModelSerializer,
        "update": PersonUpdateModelSerializer,
        "partial_update": PersonUpdateModelSerializer,
    }

    def get_serializer_class(self):
        return self.per_action_serializer.get(self.action)
