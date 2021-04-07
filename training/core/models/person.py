from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Person(models.Model):
    """
    Tabela de Pessoa.

    Atributos:
        - cpf -> string.
        - name (nome) -> string.
        - born_date (data de nascimento) -> date.
        - phones (telefones para contatos) -> lista de objetos do tipo Phone model.
        - user (conta de usuário da pessoa) -> objeto do tipo CustomUser model.
    """

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
    """
    Tabela de telefones.

    Atributos:
        - owners (pessoas com esse telefone) -> lista de objetos do tipo Person model.
        - number (número do telefone) -> objeto do tipo PhoneNumber. Biblioteca terceiros.
    """

    number = PhoneNumberField(unique=True)

    def __str__(self) -> str:
        return str(self.number)
