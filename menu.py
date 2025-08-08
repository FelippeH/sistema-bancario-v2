from system_bank import SystemBank

# função para entrada de dados com validação
def input_with_validation(prompt, cast_func=str, allow_empty=False, error_message="Entrada inválida."):
    while True:
        user_input = input(prompt).strip()
        if not user_input and not allow_empty: # verifica se a entrada está vazia
            print("❌ Entrada não pode ser vazia.")
            continue
        try:
            return cast_func(user_input)
        except Exception:
            print(error_message)

# inicia o sistema bancário
bank = SystemBank()

menu = """
========  MENU  ========
[1] Criar usuário
[2] Criar conta corrente
[3] Listar contas
[4] Depositar
[5] Sacar
[6] Extrato
[0] Sair
========================
Digite a opção desejada:
=> """

while True:
    option = input(menu).strip()

    if option == '1':
        cpf = input_with_validation("CPF: ")
        name = input_with_validation("Nome: ")
        address = input_with_validation("Endereço: ")
        password = input_with_validation("Senha: ")
        bank.create_user(cpf, name, address, password)

    elif option == '2':
        cpf = input_with_validation("CPF: ")
        password = input_with_validation("Senha: ")
        bank.create_checking_account(cpf, password)

    elif option == '3':
        cpf = input_with_validation("CPF: ")
        password = input_with_validation("Senha: ")
        bank.list_accounts(cpf, password)

    elif option == '4':
        password = input_with_validation("Senha: ")
        value = input_with_validation(
            "Informe o valor do depósito: ",
            cast_func=float,
            error_message="❌ Valor inválido. Digite um número válido."
        )
        bank.deposit(password, value)

    elif option == '5':
        password = input_with_validation("Senha: ")
        value = input_with_validation(
            "Informe o valor do saque: ",
            cast_func=float,
            error_message="❌ Valor inválido. Digite um número válido."
        )
        bank.withdrawal(password, value)

    elif option == '6':
        password = input_with_validation("Senha: ")
        bank.show_extract(password)

    elif option == '0':
        print("Saindo do sistema. Até logo!")
        break

    else:
        print("Opção inválida. Tente novamente.")