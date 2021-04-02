from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    Serializer,
)

from training.core.models import Person, Phone
from training.core.serializers.validators import is_a_valid_cpf


class PhoneSerializer(Serializer):
    id = IntegerField(read_only=True)
    number = CharField()


class PersonSerializer(ModelSerializer):
    phones = PhoneSerializer(many=True)

    class Meta:
        model = Person
        fields = ["id", "cpf", "name", "born_date", "phones", "user"]

    def validate_cpf(self, value):
        return is_a_valid_cpf(value)

    def create(self, validated_data):
        phones = validated_data.pop("phones")
        person = Person.objects.create(**validated_data)

        for phone in phones:
            # (object, bool)
            phone, _ = Phone.objects.get_or_create(**phone)
            person.phones.add(phone)

        return person


class PersonListSerializer(Serializer):
    id = IntegerField(read_only=True)
    cpf = CharField(read_only=True)
    name = CharField(read_only=True)
