from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import (
    CharField,
    DateField,
    IntegerField,
    ModelSerializer,
    Serializer,
)

from training.core.models import Person, Phone
from training.core.serializers.validators import must_be_a_valid_cpf, must_not_be_empty


class PhoneSerializer(Serializer):
    """
    Serializer para ser usado como "nested" de pessoa.

    Campos:
        - id -> int.
        - number -> string.
    """

    id = IntegerField(read_only=True)
    number = CharField()


class PersonListSerializer(Serializer):
    """
    Serializer somente leitura.

    Usado para listar vários pessoas.

    Campos:
        - id -> int.
        - cpf -> string.
        - name -> string.
    """

    id = IntegerField(read_only=True)
    cpf = CharField(read_only=True)
    name = CharField(read_only=True)


class PersonRetrieveSerializer(Serializer):
    """
    Serializer somente leitura.

    Usado para exibir uma pessoa específica.

    Campos:
        - id -> int.
        - cpf -> string.
        - name -> string.
        - born_date -> string do objeto date.
        - phones -> lista de PhoneSerializer
        - user (id do usuário) -> int.
    """

    id = IntegerField(read_only=True)
    cpf = CharField(read_only=True)
    name = CharField(read_only=True)
    born_date = DateField(read_only=True)
    phones = PhoneSerializer(many=True, read_only=True)
    user = PrimaryKeyRelatedField(read_only=True)


class PersonCreateModelSerializer(ModelSerializer):
    """
    Serializer para criar uma nova pessoa.

    Campos:
        - id (somente leitura) -> int.
        - cpf -> string.
        - name -> string.
        - born_date -> string do objeto date.
        - phones -> lista de PhoneSerializer.
        - user (id do usuário) -> int.

    Raises:
        NotImplementedError: Possui apenas o método .create(). Para usar .update(), utilize PersonUpdateModelSerializer
    """

    # Ex.: phones = [{"number":"+554791234-56789"}, {"number":"+554791234-56788"}, {"number":"+554791234-56787"}]
    phones = PhoneSerializer(many=True)

    class Meta:
        model = Person
        fields = ["id", "cpf", "name", "born_date", "phones", "user"]
        # se for um cpf inválido, retorna um erro de validação
        extra_kwargs = {"cpf": {"validators": [must_be_a_valid_cpf]}}

    def validate_phones(self, phones: list):
        # se for vazio, retorna um erro de validação
        must_not_be_empty(phones)

        return phones

    def create(self, validated_data):
        phones = validated_data.pop("phones")
        person = Person.objects.create(**validated_data)

        for phone in phones:
            # (object, bool)
            phone, _ = Phone.objects.get_or_create(**phone)
            person.phones.add(phone)

        return person

    def update(self, instance, validated_data):
        message = "This serializer must not be used for update. Instead use PersonUpdateModelSerializer."
        raise NotImplementedError(message)


class PersonUpdateModelSerializer(ModelSerializer):
    """
    Serializer para atualizar uma pessoa, parcialmente ou não.

    Campos:
        - id (somente leitura) -> int.
        - cpf -> string.
        - name -> string.
        - born_date -> string do objeto date.
        - phones -> lista de PhoneSerializer.
        - user (id do usuário) -> int.

    Raises:
        NotImplementedError: Possui apenas o método .update(). Para usar .create(), utilize PersonCreateModelSerializer
    """

    phones = PhoneSerializer(many=True)

    class Meta:
        model = Person
        fields = ["name", "phones"]

    def validate_phones(self, phones: list):
        must_not_be_empty(phones)

        return phones

    def create(self, validated_data):
        message = "This serializer must not be used for creation. Instead use PersonCreateModelSerializer."
        raise NotImplementedError(message)

    def update(self, instance, validated_data):
        phones = validated_data.pop("phones", None)
        if phones is not None:
            self.__update_phones(instance, phones)

        return super().update(instance, validated_data)

    def __update_phones(self, instance, phones):
        phones_for_update = []
        for phone in phones:
            object, _ = Phone.objects.get_or_create(**phone)
            phones_for_update.append(object)

        instance.phones.set(phones_for_update)
