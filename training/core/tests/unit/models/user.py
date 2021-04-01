from django.test import TestCase

from training.core.models import CustomUser


class CustomUserTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertTrue(hasattr(CustomUser, "email"))
        self.assertTrue(hasattr(CustomUser, "username"))
        self.assertTrue(hasattr(CustomUser, "password"))

    def test_str(self):
        custom_user = CustomUser(email="foo@bar.com", username="foobar")
        self.assertEqual(str(custom_user), custom_user.username)
