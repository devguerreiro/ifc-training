from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from training.core.models import CustomUser


class UserAPITestCase(APITestCase):
    def test_should_list_all_users(self):
        """
        Verifica se o endpoint de listagem está retornando todos os dados do banco.
        """
        quantity = 15
        # cria 15 usuários no banco de teste
        baker.make(CustomUser, _quantity=quantity)

        path = reverse("user-list")

        # faz a requisição
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # verifica se retornou todos
        self.assertEqual(len(response.data), quantity)
