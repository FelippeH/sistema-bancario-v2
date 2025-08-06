from ast import While
from models.transaction import Deposit, Withdrawal
from models.account import CheckingAccount
from models.customer import Individual
from models.history import History

customers = []
accounts = []

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

# Método para encontrar um cliente pelo CPF
# aqui eu utilizo esse método apenas no create_user
def find_customer_by_cpf_only(cpf, customers):
    for customer in customers:
        if isinstance(customer, Individual) and customer.cpf == cpf:
            return customer
    return None

# Método para encontrar um cliente pelo CPF e senha
# aqui eu utilizo esse método apenas no create_checking_account
def find_customer_by_cpf_and_password(cpf, password, customers):
    for customer in customers:
        if isinstance(customer, Individual) and customer.cpf == cpf and customer.password == password:
            return customer
    return None

# Método para encontrar um cliente apenas pela senha
# aqui eu utilizo esse método para solicitar o depósito, saque e exibir extrato. Pois como o cliente já está autenticado, não é necessário verificar o CPF.
def find_customer_by_password_only(password, customers):
    for customer in customers:
        if isinstance(customer, Individual) and customer.password == password:
            return customer
    return None

# Método para criar um novo usuário [1]
def create_user():
    cpf = input("\nInforme seu CPF: ").strip()
    customer_obj = find_customer_by_cpf_only(cpf, customers)

    if customer_obj:
        print("\n❌ Já existe um cliente com o CPF informado.")

    # Se o CPF não estiver cadastrado, solicita os dados do cliente
    else:
        name = input("Informe seu nome completo: ")
        address = input("Informe o logradouro: ")
        address += ", " + input("Informe o número: ")
        address += ", " + input("Informe o bairro: ")
        address += ", " + input("Informe a cidade: ")
        address += ", " + input("Informe o CEP: ")
        
        # verifica se a senha tem pelo menos 6 caracteres
        while True:
            password = input("\nCrie uma senha (a senha deve ter no mínmo 6 caracteres): ").strip()
            if len(password) >= 6:
                break
            print("❌ Senha muito curta. A senha deve ter no mínimo 6 caracteres.")

    new_customer = Individual(cpf=cpf, name=name, address=address, password=password)
    
    # Adiciona o novo cliente à lista de clientes
    customers.append(new_customer)
    print("\n✅ Usuário cadastrado com sucesso.")

# Método para criar uma conta corrente [2]
def create_checking_account():
    cpf = input("\nInforme o seu CPF: ").strip()
    password = input("Digite sua senha: ").strip()
    customer_obj = find_customer_by_cpf_and_password(cpf, password, customers)
    # verifica se o cliente existe, fazendo validação do CPF e senha
    if not customer_obj:
        print("\n❌ Cliente não encontrado.")
        return

    account_number = len(accounts) + 1
    new_account = CheckingAccount(number=account_number, customer=customer_obj)

    accounts.append(new_account)
    customer_obj.add_account(new_account)

    print("\n✅ Conta criada com sucesso.")

# Método para listar contas [3]
def list_accounts():
    cpf = input("\nInforme o seu CPF: ").strip()
    password = input("Digite sua senha: ").strip()
    customer_obj = find_customer_by_cpf_and_password(cpf, password, customers)

    if not customer_obj:
        print("\n❌ Cliente não encontrado.")
        return
    
# Exibe as contas cadastradas
    print("\n======= CONTAS =========")
    for account in accounts:
        print(f"Conta: {account.number}, Cliente: {account.customer.name}, Saldo: R$ {account.balance:.2f}")
    print("========================")

# método de depósito [4]
def deposit():
    password = input("\nEntre com a sua senha: ").strip()
    customer_obj = find_customer_by_password_only(password, customers)

    # Verifica se o cliente existe
    if not customer_obj:
        print(f"\n❌ Senha incorreta.")
        print("Verifique as informações, e tente novamente.")
        return
    
    # Verifica se o cliente possui contas
    if not customer_obj.accounts:
        print("\n❌ Este cliente não possui nenhuma conta corrente cadastrada.")
        return

    # Solicita o valor do depósito
    try:
        value = float(input("Digite o valor do depósito: "))
        transaction = Deposit(value) # Cria uma nova transação de depósito
        result = customer_obj.make_transactions(transaction) # Registra a transação na conta do cliente
        if result == "daily_transactions_limit_exceeded":
            print("\n❌ Erro. Limite de transações diárias atingido.")
        elif result is True:
            print(f"\n✅ Depósito de R$ {value:.2f} realizado com sucesso.")
        else:
            print("\n❌ O valor do depósito não pode ser superior a R$2.500,00.")
          
    # Captura erros de valor inválido        
    except ValueError:
        print("\n❌ O valor informado é inválido. Verifique as informações e tente novamente.")
    except Exception as e:
        print(f"\n❌ Erro ao processar depósito: {e}")

# método de saque [5]
def withdrawal():
    password = input("\nEntre com a sua senha: ").strip()
    customer_obj = find_customer_by_password_only(password, customers)

    if not customer_obj:
        print(f"\n❌ Senha incorreta.")
        print("Verifique as informações, e tente novamente.")
        return
    
    if not customer_obj.accounts:
        print("\n❌ Este cliente não possui nenhuma conta corrente cadastrada.")
        return
    
    # Solicita o valor do saque
    try:
        value = float(input("Digite o valor do saque: "))
        transaction = Withdrawal(value)  # Cria uma nova transação de saque
        result = customer_obj.make_transactions(transaction)  # Registra a transação na conta do cliente

        # Verifica o resultado do saque
        if result == "daily_transactions_limit_exceeded":
            print("\n❌ Erro. Limite de transações diárias atingido.")
        elif result is True:
            print(f"\n✅ Saque de R$ {value:.2f} realizado com sucesso.")
        elif result == "limit_exceeded":
            print("\n❌ Erro. O valor do saque é maior que o limite permitido por operação.")
        elif result == "withdrawal_exceeded":
            print("\n❌ Erro. Número máximo de saques diários atingido.")
        elif result == "insufficient_funds":
            print("\n❌ Falha! Você não tem saldo suficiente na conta. Verifique o saldo e tente novamente.")
        else:
            print("\n❌ Erro inesperado ao tentar realizar o saque.")

    # Captura erros de valor inválido    
    except ValueError:
        print("\n❌ O valor informado é inválido. Verifique as informações e tente novamente.")
    except Exception as e:
        print(f"\n❌ Erro ao processar saque: {e}")
    
# método de extrato [6]
def show_extract():
    password = input("\nEntre com a sua senha: ").strip()
    account = find_customer_by_password_only(password, customers)

    # Verifica se o cliente existe
    if not account:
        print(f"\n❌ Senha incorreta.")
        print("Verifique as informações, e tente novamente.")
        return
    # Verifica se o cliente possui contas
    if not account.accounts:
        print("\n❌ Este cliente não possui nenhuma conta corrente cadastrada.")
        return

    # Exibe o histórico de transações da primeira conta do cliente
    account = account.accounts[0]
    print("\n======= EXTRATO ========")
    account.history.show()
    print(f"\nSaldo atual: R$ {account.balance:.2f}")
    print("========================")

# Loop principal do menu
while True:
    opcao = input(menu).strip()

    if opcao == "1":
        create_user()
        
    elif opcao == "2":
        create_checking_account()
        
    elif opcao == "3":
        list_accounts()
        
    elif opcao == "4":
        deposit()
        
    elif opcao == "5":
        withdrawal()
        
    elif opcao == "6":
        show_extract()
        
    elif opcao == "0":
        print("\nSaindo do sistema...")
        break
    
    else:
        print("\n❌ Opção inválida. Tente novamente.")