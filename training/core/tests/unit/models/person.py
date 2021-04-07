from django.test import TestCase
from model_bakery import baker

from training.core.models import Person, Phone


class PersonTestCase(TestCase):
    def test_should_has_all_attributes(self):
        """
        Verifica se a model tem todos os atributos necessários.
        """
        self.assertTrue(hasattr(Person, "cpf"))
        self.assertTrue(hasattr(Person, "name"))
        self.assertTrue(hasattr(Person, "born_date"))
        self.assertTrue(hasattr(Person, "phones"))
        self.assertTrue(hasattr(Person, "user"))

    def test_str_should_return_person_name(self):
        """
        Verifica se quando o objeto é convertido para string, retorna o nome da pessoa.
        """
        person = baker.prepare(Person)
        self.assertEqual(str(person), person.name)


class PhoneTestCase(TestCase):
    def test_should_has_all_attributes(self):
        """
        Verifica se a model tem todos os atributos necessários.
        """
        self.assertTrue(hasattr(Phone, "owners"))
        self.assertTrue(hasattr(Phone, "number"))

    def test_str_should_return_phone_number(self):
        """
        Verifica se quando o objeto é convertido para string, retorna o número do telefone.
        """
        phone = Phone(number="+554791234-5678")
        self.assertEqual(str(phone), str(phone.number))
