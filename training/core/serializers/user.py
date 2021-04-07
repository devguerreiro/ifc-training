from rest_framework.serializers import CharField, EmailField, IntegerField, Serializer


class UserReadOnlySerializer(Serializer):
    """
    Serializer somente leitura.

    Usado para listar vários usuários ou exibir somente um específico.

    Campos:
        - id -> int
        - email -> string
        - username -> string
    """

    id = IntegerField(read_only=True)
    email = EmailField(read_only=True)
    username = CharField(read_only=True)
