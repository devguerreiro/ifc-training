from rest_framework.serializers import ValidationError
from validate_docbr import CPF

cpf_validator = CPF()


def must_be_a_valid_cpf(cpf: str):
    """
    Deve ser um cpf válido seguindo a fórmula de cálculo do dígito verificador.
    """
    if not cpf_validator.validate(cpf):
        raise ValidationError("This is a invalid cpf.")


def must_not_be_empty(field):
    """
    O campo não deve ser vazio. Ex.: "", [], {}.
    """
    if not isinstance(field, bool) and field is not None:
        if not field:
            raise ValidationError("This field must not be empty.")
