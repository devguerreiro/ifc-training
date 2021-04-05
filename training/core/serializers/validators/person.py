from validate_docbr import CPF

cpf_validator = CPF()


def is_a_valid_cpf(cpf: str) -> bool:
    return cpf_validator.validate(cpf)
