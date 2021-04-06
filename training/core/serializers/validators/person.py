from rest_framework.serializers import ValidationError
from validate_docbr import CPF

cpf_validator = CPF()


def is_a_valid_cpf(cpf: str):
    if not cpf_validator.validate(cpf):
        raise ValidationError("This is a invalid cpf.")


def phones_is_empty(phones: list):
    if phones is not None and not phones:
        raise ValidationError("This field must not be empty.")
