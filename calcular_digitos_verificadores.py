def calcula_digitos_verificadores(cpf_base):
    # Verifica se a cpf_base possui 9 dígitos
    if len(cpf_base) != 9 or not cpf_base.isdigit():
        return "CPF base inválido"

    # Calcula o primeiro dígito verificador
    soma = sum(int(cpf_base[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    digito1 = 0 if resto == 10 or resto == 11 else resto

    # Calcula o segundo dígito verificador
    soma = sum(int(cpf_base[i]) * (11 - i) for i in range(9))
    soma += digito1 * 2
    resto = (soma * 10) % 11
    digito2 = 0 if resto == 10 or resto == 11 else resto

    return f"{digito1}{digito2}"

# Exemplo de uso
cpf_base_input = input("Digite os nove primeiros dígitos do CPF: ")

resultado = calcula_digitos_verificadores(cpf_base_input)
print(f"Os dois últimos dígitos do CPF são: {resultado}")


#teste teste
