from django.test import TestCase
from model_bakery import baker

from training.core.models import CustomUser


class CustomUserTestCase(TestCase):
    def test_should_has_all_attributes(self):
        """
        Verifica se a model tem todos os atributos necessários.
        """
        self.assertTrue(hasattr(CustomUser, "email"))
        self.assertTrue(hasattr(CustomUser, "username"))
        self.assertTrue(hasattr(CustomUser, "password"))

    def test_str_should_return_user_username(self):
        """
        Verifica se quando o objeto é convertido para string, retorna o nome de usuário do usuário.
        """
        custom_user = baker.prepare(CustomUser)
        self.assertEqual(str(custom_user), custom_user.username)
