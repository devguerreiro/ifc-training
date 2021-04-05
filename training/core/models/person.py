from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Person(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=200)

    # YYYY-MM-DD
    born_date = models.DateField()

    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ForeignKey.related_name
    phones = models.ManyToManyField(
        "core.Phone", related_name="owners", related_query_name="owner"
    )
    user = models.OneToOneField(
        "core.CustomUser", related_name="info", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name


class Phone(models.Model):
    number = PhoneNumberField(unique=True)

    def __str__(self) -> str:
        return str(self.number)
