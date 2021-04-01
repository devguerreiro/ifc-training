from rest_framework.serializers import CharField, EmailField, IntegerField, Serializer


class UserListSerializer(Serializer):
    id = IntegerField()
    email = EmailField()
    username = CharField()
