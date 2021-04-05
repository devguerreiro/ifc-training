from rest_framework.serializers import ValidationError
from validate_docbr import CPF

cpf_validator = CPF()


def is_a_valid_cpf(cpf: str) -> bool:
    if not cpf_validator.validate(cpf):
        raise ValidationError("Invalid cpf.")
