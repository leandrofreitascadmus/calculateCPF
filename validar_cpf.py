def valida_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False, "CPF deve ter 11 dígitos"

    # Calcula o primeiro dígito verificador
    soma = 0
    peso = 10
    for digit in cpf[:9]:
        soma += int(digit) * peso
        peso -= 1

    resto = (soma * 10) % 11
    if resto == 10 or resto == 11:
        resto = 0

    if resto != int(cpf[9]):
        return False, "CPF inválido"

    # Calcula o segundo dígito verificador
    soma = 0
    peso = 11
    for digit in cpf[:10]:
        soma += int(digit) * peso
        peso -= 1

    resto = (soma * 10) % 11
    if resto == 10 or resto == 11:
        resto = 0

    if resto != int(cpf[10]):
        return False, "CPF inválido"

    return True, "CPF válido"

# Exemplo de uso
cpf_input = input("Digite o CPF: ")
valido, mensagem = valida_cpf(cpf_input)

if valido:
    print("CPF válido.")
else:
    print("CPF inválido. Motivo:", mensagem)