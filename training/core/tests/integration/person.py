from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APITestCase

from training.core.models import Person, Phone
from training.core.serializers import PhoneSerializer


class PersonAPITestCase(APITestCase):
    def test_should_return_all_from_database(self):
        # cria 10 pessoas no banco de teste
        baker.make("core.Person", _quantity=10)

        path = reverse("person-list")

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_should_return_person_with_id_1(self):
        baker.make("core.Person", id=1)

        # api/v1/person/1
        path = reverse("person-detail", args=[1])

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data.get("id"), 1)

    def test_should_create_a_person(self):
        user = baker.make("core.CustomUser")
        data = {
            "cpf": "54569360033",
            "name": "foobar",
            "born_date": "2001-01-01",
            "phones": [{"number": "+554791234-5678"}],
            "user": user.id,
        }

        path = reverse("person-list")

        response = self.client.post(path, data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 1)

    def test_should_update_person_with_id_1(self):
        phone = Phone.objects.create(number="+554791234-5678")
        person = baker.make(Person, id=1, cpf="14895038033")
        person.phones.set([phone])

        new_name = "foobar"
        data = {
            "cpf": person.cpf,
            "name": new_name,
            "born_date": str(person.born_date),
            "phones": [
                {
                    "number": str(phone),
                },
            ],
            "user": person.user_id,
        }

        path = reverse("person-detail", args=[1])

        response = self.client.put(path, data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        self.assertEqual(response.data.get("cpf"), person.cpf)
        self.assertEqual(response.data.get("born_date"), str(person.born_date))
        self.assertEqual(response.data.get("user"), person.user_id)

        phones = PhoneSerializer(instance=person.phones.all(), many=True)
        self.assertEqual(response.data.get("phones"), phones.data)

        person.refresh_from_db()
        self.assertEqual(person.name, new_name)
