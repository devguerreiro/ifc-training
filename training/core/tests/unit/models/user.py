from django.test import TestCase

from training.core.models import CustomUser

class CustomUserTestCase(TestCase):
    def test_has_all_attributes(self):
        custom_user = CustomUser()
        self.assertTrue(hasattr(custom_user, "email"))
        self.assertTrue(hasattr(custom_user, "username"))
        self.assertTrue(hasattr(custom_user, "password"))

    def test_str(self):
        custom_user = CustomUser(email="foo@bar.com", username="foobar")
        self.assertEqual(str(custom_user), custom_user.username)