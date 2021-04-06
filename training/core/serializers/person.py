from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import (
    CharField,
    DateField,
    IntegerField,
    ModelSerializer,
    Serializer,
)

from training.core.models import Person, Phone
from training.core.serializers.validators import is_a_valid_cpf, phones_is_empty


class PhoneSerializer(Serializer):
    id = IntegerField(read_only=True)
    number = CharField()


class PersonUpdateModelSerializer(ModelSerializer):
    phones = PhoneSerializer(many=True)

    class Meta:
        model = Person
        fields = ["name", "phones"]

    def validate_phones(self, phones: list):
        phones_is_empty(phones)

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
        # phones = []
        if not phones:
            instance.phones.set(phones)
        else:
            phones_for_update = []
            # phones = [{"number":"+554791234-56789"}, {"number":"+554791234-56788"}, {"number":"+554791234-56787"}]
            for phone in phones:
                object, _ = Phone.objects.get_or_create(**phone)
                phones_for_update.append(object)
            instance.phones.set(phones_for_update)


class PersonCreateModelSerializer(ModelSerializer):
    # phones = [{"number":"+554791234-56789"}, {"number":"+554791234-56788"}, {"number":"+554791234-56787"}]
    phones = PhoneSerializer(many=True)

    class Meta:
        model = Person
        fields = ["id", "cpf", "name", "born_date", "phones", "user"]
        extra_kwargs = {"cpf": {"validators": [is_a_valid_cpf]}}

    def validate_phones(self, phones: list):
        phones_is_empty(phones)

        return phones

    def create(self, validated_data):
        phones = validated_data.pop("phones")
        person = Person.objects.create(**validated_data)

        for phone in phones:
            # (object, bool)
            phone, _ = Phone.objects.get_or_create(**phone)
            person.phones.add(phone)

        # retorna um objeto do tipo model Person
        return person

    def update(self, instance, validated_data):
        message = "This serializer must not be used for update. Instead use PersonUpdateModelSerializer."
        raise NotImplementedError(message)


class PersonListSerializer(Serializer):
    id = IntegerField(read_only=True)
    cpf = CharField(read_only=True)
    name = CharField(read_only=True)


class PersonRetrieveSerializer(Serializer):
    id = IntegerField(read_only=True)
    cpf = CharField(read_only=True)
    name = CharField(read_only=True)
    born_date = DateField(read_only=True)
    phones = PhoneSerializer(many=True)
    user = PrimaryKeyRelatedField(read_only=True)
