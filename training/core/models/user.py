from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Tabela de usuários.

    Atributos:
        - herda todos de AbstractUser.
        - email -> string com validação de email.

    USERNAME_FIELD = "email" -> login através do email.
    REQUIRED_FIELDS = ["username"] -> campos obrigatórios quando chamar .create().
    """

    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.username
