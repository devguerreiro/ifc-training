from django.test import TestCase
from model_bakery import baker

from training.core.models import Phone
from training.core.serializers import (
    PersonListSerializer,
    PersonRetrieveSerializer,
    PhoneSerializer,
)


class PhoneSerializerTestCase(TestCase):
    def test_should_has_all_attributes(self):
        phone = Phone.objects.create(number="+554791234-5678")
        serializer = PhoneSerializer(instance=phone)

        self.assertIsNotNone(serializer.data.get("id"))
        self.assertIsNotNone(serializer.data.get("number"))


class PersonListSerializerTestCase(TestCase):
    def test_should_has_all_attributes(self):
        person = baker.make("core.Person")
        serializer = PersonListSerializer(instance=person)

        self.assertIsNotNone(serializer.data.get("id"))
        self.assertIsNotNone(serializer.data.get("cpf"))
        self.assertIsNotNone(serializer.data.get("name"))


class PersonRetrieveSerializerTestCase(TestCase):
    def test_should_has_all_attributes(self):
        person = baker.make("core.Person")
        serializer = PersonRetrieveSerializer(instance=person)

        self.assertIsNotNone(serializer.data.get("id"))
        self.assertIsNotNone(serializer.data.get("cpf"))
        self.assertIsNotNone(serializer.data.get("name"))
        self.assertIsNotNone(serializer.data.get("born_date"))
        self.assertIsNotNone(serializer.data.get("phones"))
        self.assertIsNotNone(serializer.data.get("user"))
