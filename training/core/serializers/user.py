from rest_framework.serializers import CharField, EmailField, IntegerField, Serializer


class UserReadOnlySerializer(Serializer):
    id = IntegerField(read_only=True)
    email = EmailField(read_only=True)
    username = CharField(read_only=True)
