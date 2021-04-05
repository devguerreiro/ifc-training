from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    Serializer,
)

from training.core.models import Person, Phone
from training.core.serializers.validators import is_a_valid_cpf, phones_is_empty


class PhoneSerializer(Serializer):
    id = IntegerField(read_only=True)
    number = CharField()


class PersonModelSerializer(ModelSerializer):
    # phones = [{"number":"+554791234-56789"}, {"number":"+554791234-56788"}, {"number":"+554791234-56787"}]
    phones = PhoneSerializer(many=True)

    class Meta:
        model = Person
        fields = ["id", "cpf", "name", "born_date", "phones", "user"]
        extra_kwargs = {"cpf": {"validators": [is_a_valid_cpf, phones_is_empty]}}

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


class PersonReadOnlySerializer(Serializer):
    id = IntegerField(read_only=True)
    cpf = CharField(read_only=True)
    name = CharField(read_only=True)
