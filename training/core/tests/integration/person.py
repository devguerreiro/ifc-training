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
    def test_should_list_all_people(self):
        """
        Verifica se o endpoint de listagem está retornando todos os dados do banco.
        """
        quantity = 10
        # cria 10 pessoas no banco de teste
        baker.make("core.Person", _quantity=quantity)

        path = reverse("person-list")

        # faz a requisição
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # verifica se retornou todos
        self.assertEqual(len(response.data), quantity)

    def test_should_retrieve_a_person(self):
        """
        Verifica se o endpoint de recuperação está retornando a pessoa com o id informado.
        """
        person = baker.make("core.Person")

        path = reverse("person-detail", args=[person.id])

        # faz a requisição
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # verifica se retornou os dados da pessoa
        self.assertEqual(response.data.get("id"), person.id)

    def test_should_return_404_person_not_found(self):
        """
        Verifica se os endpoints de recuperação, atualização e remoção retorna 404, caso o id não exista.
        """
        path = reverse("person-detail", args=[1])

        # faz a requisição
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

        # faz a requisição
        response = self.client.put(path)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

        # faz a requisição
        response = self.client.patch(path)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

        # faz a requisição
        response = self.client.delete(path)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_should_create_a_person(self):
        """
        Verifica se o endpoint de criação cadastra no banco de dados, caso os dados sejam válidos.
        """
        user = baker.make("core.CustomUser")
        data = {
            # cpf aleatório válido
            "cpf": "54569360033",
            "name": "foobar",
            "born_date": "2001-01-01",
            "phones": [{"number": "+554791234-5678"}],
            "user": user.id,
        }

        path = reverse("person-list")

        # faz a requisição
        response = self.client.post(path, data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # verifica se a pessoa foi cadastrada no banco de dados
        self.assertEqual(Person.objects.count(), 1)

    def test_should_update_a_person(self):
        """
        Verifica se o endpoint de atualização atualiza no banco de dados, caso os dados sejam válidos.
        """
        person = baker.make(Person, name="foobar")
        phone = Phone.objects.create(number="+554791234-5678")

        person.phones.set([phone])

        # atributo a ser atualizado
        new_name = "new name"
        data = {
            "name": new_name,
            "phones": [
                {
                    "number": str(phone),
                },
            ],
        }

        path = reverse("person-detail", args=[person.id])

        # faz a requisição
        response = self.client.put(path, data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        person.refresh_from_db()
        # verifica se a versão mais recente do dado no banco, tem o nome atualizado.
        self.assertEqual(person.name, new_name)

    def test_should_partial_update_a_person(self):
        """
        Verifica se o endpoint de atualização parcial atualiza no banco de dados, caso os dados sejam válidos.
        """
        person = baker.make("core.Person", name="foobar")

        new_name = "nome atualizado"
        data = {"name": new_name}

        path = reverse("person-detail", args=[person.id])

        # faz a requisição
        response = self.client.patch(path, data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        person.refresh_from_db()
        # verifica se a versão mais recente do dado no banco, tem o nome atualizado.
        self.assertEqual(person.name, new_name)

    def test_should_not_create_a_person_with_invalid_cpf(self):
        """
        Verifica se o endpoint de criação não cria no banco de dados, caso o cpf seja inválido.
        """
        user = baker.make("core.CustomUser")
        data = {
            # cpf inválido
            "cpf": "12345678910",
            "name": "foobar",
            "born_date": "2001-01-01",
            "phones": [{"number": "+554791234-5678"}],
            "user": user.id,
        }

        path = reverse("person-list")

        # faz a requisição
        response = self.client.post(path, data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # verifica se a pessoa não foi criada no banco de dados
        self.assertEqual(Person.objects.count(), 0)

    def test_should_not_create_a_person_with_empty_phones(self):
        """
        Verifica se o endpoint de criação não cria no banco de dados, caso não seja informado nenhum telefone.
        """
        user = baker.make("core.CustomUser")
        data = {
            "cpf": "54569360033",
            "name": "foobar",
            "born_date": "2001-01-01",
            # nenhum telefone informado
            "phones": [],
            "user": user.id,
        }

        path = reverse("person-list")

        # faz a requisição
        response = self.client.post(path, data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # verifica se a pessoa não foi criada no banco de dados
        self.assertEqual(Person.objects.count(), 0)

    def test_should_not_update_a_person_with_empty_phones(self):
        """
        Verifica se o endpoint de atualização não atualiza no banco de dados, caso não seja informado nenhum telefone.
        """
        person = baker.make("core.Person")
        person_old_name = person.name

        data = {
            "name": person_old_name,
            # nenhum telefone informado
            "phones": [],
        }

        path = reverse("person-detail", args=[person.id])

        # faz a requisição
        response = self.client.put(path, data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        person.refresh_from_db()
        # verifica se a versão mais recente no banco de dados, tem o mesmo nome.
        self.assertEqual(person.name, person_old_name)

    def test_should_not_partial_update_a_person_with_empty_phones(self):
        """
        Verifica se o endpoint de atualização não atualiza no banco de dados, caso não seja informado nenhum telefone.
        """
        person = baker.make("core.Person")
        phone = Phone.objects.create(number="+554791234-5678")

        person.phones.set([phone])
        person_old_phones = person.phones

        data = {"phones": []}

        path = reverse("person-detail", args=[person.id])

        # faz a requisição
        response = self.client.patch(path, data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        person.refresh_from_db()
        # verifica se a versão mais recente no banco de dados, tem os mesmos telefones.
        self.assertEqual(person.phones, person_old_phones)

    def test_should_remove_a_person(self):
        """
        Verifica se o endpoint de remoção está removendo a pessoa com o id informado.
        """
        person = baker.make("core.Person")

        path = reverse("person-detail", args=[person.id])

        # confirma que a pessoa está cadastrada no banco de dados
        self.assertEqual(Person.objects.count(), 1)

        # faz a requisição
        response = self.client.delete(path)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # verifica se a pessoa foi removida do banco de dados
        self.assertEqual(Person.objects.count(), 0)
