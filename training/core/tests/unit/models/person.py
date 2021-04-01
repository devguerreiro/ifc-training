from django.test import TestCase

from training.core.models import Person, Phone


class PersonTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertTrue(hasattr(Person, "cpf"))
        self.assertTrue(hasattr(Person, "name"))
        self.assertTrue(hasattr(Person, "born_date"))
        self.assertTrue(hasattr(Person, "phones"))
        self.assertTrue(hasattr(Person, "user"))

    def test_str(self):
        person = Person()
        self.assertEqual(str(person), person.name)


class PhoneTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertTrue(hasattr(Phone, "number"))

    def test_str(self):
        phone = Phone()
        self.assertEqual(str(phone), phone.number)
