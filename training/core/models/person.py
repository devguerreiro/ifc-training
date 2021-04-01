from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Person(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=200)
    born_date = models.DateField()
    # related name é um atributo para fazer a relação inversa.
    # Por exemplo: phone.owners.count() -> retorna quantas "pessoas" tem esse número cadastrado
    fone = models.ManyToManyField("core.Phone", related_name="owners", related_query_name="owner")
    user = models.OneToOneField("core.CustomUser", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Phone(models.Model):
    number = PhoneNumberField()
    
    def __str__(self):
        return self.number