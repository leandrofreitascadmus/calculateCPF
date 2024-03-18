def calcula_digitos_verificadores(cpf_base):
    # Verifica se a cpf_base possui 9 dígitos
    if len(cpf_base) != 9 or not cpf_base.isdigit():
        return "CPF base inválido"

    # Calcula o primeiro e segundo dígito verificador
    dvs = []
    for n in range(10, 12):
        soma = sum([int(cpf_base[i])*(n-i) for i in range(len(cpf_base))])
        soma %= 11
        dv = 0 if soma < 2 else 11 - soma
        dvs.append(str(dv))
        cpf_base += str(dv)

    return "".join(dvs)

def verifica_cpf(cpf):
    if len(cpf) != 11 or not cpf.isdigit():
        return "CPF inválido"
    cpf_base = cpf[:9]
    cpf_dv = cpf[-2:]

    # verifica se digitos verificadores são iguais aos calculados
    return cpf_base + calcula_digitos_verificadores(cpf_base) == cpf

# Exemplo de uso
cpf_base_user_input = input("Digite os nove primeiros dígitos do CPF: ")

resultado = verifica_cpf(cpf_base_user_input)
print(f"Os dois últimos dígitos do CPF são: {resultado}")

#teste
