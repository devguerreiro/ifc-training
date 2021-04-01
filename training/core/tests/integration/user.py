from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK
from django.urls import reverse

from model_bakery import baker

from training.core.models import CustomUser


class UserAPITestCase(APITestCase):
    def test_should_return_all_users(self):
        # criado 15 usuários
        quantity = 15
        baker.make(CustomUser, _quantity=quantity)
        
        url = reverse("user-list") # localhost:8000/api/v1/user

        response = self.client.get(path=url) # aqui onde a requisição é feita

        # deve retornar status 200 OK
        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar 15 usuários
        self.assertEqual(len(response.data), quantity)
