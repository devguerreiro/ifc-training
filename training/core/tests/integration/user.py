from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from training.core.models import CustomUser


class UserAPITestCase(APITestCase):
    def test_should_return_all_users(self):
        # criado 15 usuários
        quantity = 15
        baker.make(CustomUser, _quantity=quantity)

        # localhost:8000/api/v1/user
        url = reverse("user-list")

        # aqui onde a requisição é feita
        response = self.client.get(path=url)

        # deve retornar status 200 OK
        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar 15 usuários
        self.assertEqual(len(response.data), quantity)
