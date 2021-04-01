from rest_framework.serializers import Serializer, EmailField, IntegerField, CharField


class UserListSerializer(Serializer):
    id = IntegerField()
    email = EmailField()
    username = CharField()
