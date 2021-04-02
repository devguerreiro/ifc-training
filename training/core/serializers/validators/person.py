from rest_framework.serializers import ValidationError
from validate_docbr import CPF


def is_a_valid_cpf(cpf: str) -> bool:
    if not CPF().validate(cpf):
        raise ValidationError("CPF invalid")
