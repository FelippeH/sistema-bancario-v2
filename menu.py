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
=> """

# Função auxiliar para encontrar um cliente pelo CPF
def find_customer_by_cpf(cpf, customers):
    for customer in customers:
        if isinstance(customer, Individual) and customer.cpf == cpf:
            return customer
    return None

# Método para criar um novo usuário [1]
def create_user():
    cpf = input("Digite seu CPF: ").strip()
    customer = find_customer_by_cpf(cpf, customers)
    
    # Verifica se o CPF já está cadastrado
    if customer:
        print("\n❌ Já existe um cliente com o CPF informado.")
        
    # Se o CPF não estiver cadastrado, solicita os dados do cliente
    else:
        name = input("Digite seu nome: ")
        address = input("Digite seu endereco: ")
        password = input("Crie uma senha: ")
        
    new_customer = Individual(cpf=cpf, name=name, address=address)
    new_customer.password = password
    
    # Adiciona o novo cliente à lista de clientes
    customers.append(new_customer)
    print("\n✅ Usuário cadastrado com sucesso.")

# Método para criar uma conta corrente [2]
def create_checking_account():
    cpf = input("Informe o CPF do cliente: ").strip()
    customer = find_customer_by_cpf(cpf, customers)

    if not customer:
        print("❌ Cliente não encontrado.")
        return

    account_number = len(accounts) + 1
    new_account = CheckingAccount(number=account_number, customer=customer)

    accounts.append(new_account)
    customer.add_account(new_account)

    print("✅ Conta criada com sucesso.")

# Método para listar contas [3]
def list_accounts():
    if not accounts:
        print("\n❌ Nenhuma conta corrente cadastrada.")
        return
    if not customers:
        print("\n❌ Nenhum cliente cadastrado.")
        return
    
# Exibe as contas cadastradas
    print("\n======= CONTAS =======")
    for account in accounts:
        print(f"Conta: {account.number}, Cliente: {account.customer.name}, Saldo: R$ {account.balance:.2f}")

# método de depósito [4]
def deposit():
    cpf = input("Digite seu CPF: ").strip()
    customer_obj = find_customer_by_cpf(cpf, customers)

    # Verifica se o cliente existe
    if not customer_obj:
        print(f"\n❌ Nenhum usuário encontrado com o CPF: {cpf}.")
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
        success = customer_obj.make_transactions(transaction) # Registra a transação na conta do cliente
        if success:
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
    cpf = input("Digite seu CPF: ").strip()
    customer_obj = find_customer_by_cpf(cpf, customers)

    if not customer_obj:
        print(f"\n❌ Nenhum usuário encontrado com o CPF: {cpf}.")
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
        if result is True:
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
    cpf = input("Digite seu CPF: ").strip()
    account = find_customer_by_cpf(cpf, customers)

    # Verifica se o cliente existe
    if not account:
        print(f"\n❌ Nenhum usuário encontrado com o CPF: {cpf}.")
        print("Verifique as informações, e tente novamente.")
        return
    # Verifica se o cliente possui contas
    if not account.accounts:
        print("\n❌ Este cliente não possui nenhuma conta corrente cadastrada.")
        return

    # Exibe o histórico de transações da primeira conta do cliente
    account = account.accounts[0]
    print("\n======= EXTRATO =======")
    account.history.show()
    print(f"\nSaldo atual: R$ {account.balance:.2f}")

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