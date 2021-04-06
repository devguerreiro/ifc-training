from django.urls import reverse
from model_bakery import baker
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APITestCase

from training.core.models import Person, Phone


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

    def test_should_return_404_person_not_found(self):
        path = reverse("person-detail", args=[1])

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_should_create_a_valid_person(self):
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
        person = baker.make(Person, id=1, name="foobar")
        person.phones.set([phone])

        new_name = "new name"
        data = {
            "name": new_name,
            "phones": [
                {
                    "number": str(phone),
                },
            ],
        }

        path = reverse("person-detail", args=[1])

        response = self.client.put(path, data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        person.refresh_from_db()
        self.assertEqual(person.name, new_name)

    def test_should_partial_update_a_person_with_id_1(self):
        person = baker.make("core.Person", id=1, name="foobar")

        new_name = "nome atualizado"
        data = {"name": new_name}

        # api/v1/person/1
        path = reverse("person-detail", args=[1])

        response = self.client.patch(path, data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        person.refresh_from_db()
        self.assertEqual(person.name, new_name)

    def test_should_not_create_a_person_with_invalid_cpf(self):
        user = baker.make("core.CustomUser")
        data = {
            "cpf": "invalid cpf",
            "name": "foobar",
            "born_date": "2001-01-01",
            "phones": [{"number": "+554791234-5678"}],
            "user": user.id,
        }

        path = reverse("person-list")

        response = self.client.post(path, data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(Person.objects.count(), 0)

    def test_should_not_create_a_person_with_empty_phones(self):
        user = baker.make("core.CustomUser")
        data = {
            "cpf": "54569360033",
            "name": "foobar",
            "born_date": "2001-01-01",
            "phones": [],
            "user": user.id,
        }

        path = reverse("person-list")

        response = self.client.post(path, data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(Person.objects.count(), 0)

    def test_should_not_update_a_person_with_empty_phones(self):
        person = baker.make("core.Person")
        data = {"name": person.name, "phones": []}

        path = reverse("person-detail", args=[person.id])

        response = self.client.put(path, data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_should_not_partial_update_a_person_with_empty_phones(self):
        person = baker.make("core.Person")
        data = {"phones": []}

        path = reverse("person-detail", args=[person.id])

        response = self.client.patch(path, data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_should_remove_a_person(self):
        person = baker.make("core.Person")

        path = reverse("person-detail", args=[person.id])

        self.assertEqual(Person.objects.count(), 1)

        response = self.client.delete(path)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)

    def test_should_not_remove_a_person_that_does_not_exist(self):
        path = reverse("person-detail", args=[1])

        response = self.client.delete(path)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
