from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    Serializer,
    ValidationError,
)

from training.core.models import Person, Phone
from training.core.serializers.validators import is_a_valid_cpf


class PhoneSerializer(Serializer):
    id = IntegerField(read_only=True)
    number = CharField()


class PersonModelSerializer(ModelSerializer):
    phones = PhoneSerializer(many=True)

    class Meta:
        model = Person
        fields = ["id", "cpf", "name", "born_date", "phones", "user"]

    def validate_cpf(self, cpf):
        if not is_a_valid_cpf(cpf):
            raise ValidationError("Invalid cpf.")

        # outras possíveis validações
        # elif ...

        return cpf

    def create(self, validated_data):
        phones = validated_data.pop("phones")
        person = Person.objects.create(**validated_data)

        for phone in phones:
            # (object, bool)
            phone, _ = Phone.objects.get_or_create(**phone)
            person.phones.add(phone)

        # retorna um objeto do tipo model Person
        return person


class PersonReadOnlySerializer(Serializer):
    id = IntegerField(read_only=True)
    cpf = CharField(read_only=True)
    name = CharField(read_only=True)
