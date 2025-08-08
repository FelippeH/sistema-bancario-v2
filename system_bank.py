from models.account import CheckingAccount
from models.customer import Individual
from models.transaction import Deposit, Withdrawal
from services.customer_service import CustomerService
from utils.log import transaction_log


class SystemBank:
    def __init__(self):
        self.bank_customers = []
        self.bank_accounts = []
        self.customer_service = CustomerService()

    # Método para criar um novo usuário [1]
    # ele requisita o cpf, nome, endereço e senha do usuário no menu.py
    @transaction_log
    def create_user(self, cpf, name, address, password):
        if self.customer_service.find_by_cpf_only(cpf):
            print("\n❌ Já existe um cliente com o CPF informado.")
            return "Error"

        new_customer = Individual(
            cpf=cpf, name=name, address=address, password=password
        )
        # Adiciona o novo cliente à lista
        self.customer_service.add_customer(new_customer)
        print("\n✅ Usuário cadastrado com sucesso.")
        return "Success"

    # Método para criar uma conta corrente [2]
    @transaction_log
    def create_checking_account(self, cpf, password):
        customer_obj = self.customer_service.find_by_cpf_and_password(cpf, password)
        if not customer_obj:
            print("\n❌ Cliente não encontrado.")
            print("\n❌ Verifique as informações e tente novamente.")
            return "Error"

        account_number = len(self.bank_accounts) + 1
        new_account = CheckingAccount(number=account_number, customer=customer_obj)

        # Adiciona a nova conta à lista de contas do banco
        self.bank_accounts.append(new_account)
        # Adiciona a nova conta à lista de contas do cliente
        customer_obj.add_account(new_account)

        print("\n✅ Conta criada com sucesso.")
        return "Success"

    # Método para listar contas [3]
    @transaction_log
    def list_accounts(self, cpf, password):
        customer_obj = self.customer_service.find_by_cpf_and_password(cpf, password)

        if not customer_obj:
            print("\n❌ Verifique as informações e tente novamente.")
            return "Error"

        if not customer_obj.accounts:
            print("\n❌ Nenhuma conta cadastrada.")
            print("\n❌ Verifique as informações e tente novamente.")
            return "Error"

        # Exibe as contas cadastradas
        print("\n======= CONTAS =========")
        for account in customer_obj.accounts:
            print(
                f"Conta: {account.number}, "
                f"Cliente: {account.customer.name}, "
                f"Saldo: R$ {account.balance:.2f}"
            )
        print("========================")

        return "Success"

    # método de depósito [4]
    @transaction_log
    def deposit(self, password, value):
        customer_obj = self.customer_service.find_by_password_only(password)

        # Verifica se o cliente existe
        if not customer_obj:
            print("\n❌ Senha incorreta.")
            print("Verifique as informações, e tente novamente.")
            return "Error"

        # Verifica se o cliente possui contas
        if not customer_obj.accounts:
            print("\n❌ Este cliente não possui nenhuma conta corrente cadastrada.")
            return "Error"

        # Solicita o valor do depósito
        transaction = Deposit(value)
        # Registra a transação na conta do cliente
        result = customer_obj.make_transactions(transaction)
        if result == "daily_transactions_limit_exceeded":
            print("\n❌ Limite de transações diárias atingido.")
            return "Error"
        elif result is True:
            print(f"\n✅ Depósito de R$ {value:.2f} realizado com sucesso.")
            return "Success"
        else:
            print("\n❌ O valor do depósito não pode ser superior a R$2.500,00.")
            return "Error"

    # método de saque [5]
    @transaction_log
    def withdrawal(self, password, value):
        customer_obj = self.customer_service.find_by_password_only(password)

        if not customer_obj:
            print("\n❌ Senha incorreta.")
            print("Verifique as informações, e tente novamente.")
            return "Error"

        if not customer_obj.accounts:
            print("\n❌ Este cliente não possui nenhuma conta corrente cadastrada.")
            return "Error"

        # Solicita o valor do saque
        transaction = Withdrawal(value)
        # Registra a transação na conta do cliente
        result = customer_obj.make_transactions(transaction)

        # Verifica o resultado do saque
        if result == "daily_transactions_limit_exceeded":
            print("\n❌ Limite de transações diárias atingido.")
            return "Error"
        elif result == "limit_exceeded":
            print("\n❌ O valor do saque é maior que o limite permitido por operação.")
            return "Error"
        elif result == "withdrawal_exceeded":
            print("\n❌ Número máximo de saques diários atingido.")
            return "Error"
        elif result == "insufficient_funds":
            print("\n❌ Falha! Você não tem saldo suficiente na conta.)")
            print("(Verifique o saldo e tente novamente.")
            return "Error"
        elif result is True:
            print(f"\n✅ Saque de R$ {value:.2f} realizado com sucesso.")
            return "Success"
        else:
            print("\n❌ Error inesperado ao tentar realizar o saque.")
            return "Error"

    # método de extrato [6]
    @transaction_log
    def show_extract(self, password):
        customer_obj = self.customer_service.find_by_password_only(password)

        # Verifica se o cliente existe
        if not customer_obj:
            print("\n❌ Senha incorreta.")
            print("Verifique as informações, e tente novamente.")
            return "Error"
        # Verifica se o cliente possui contas
        if not customer_obj.accounts:
            print("\n❌ Este cliente não possui nenhuma conta corrente cadastrada.")
            return "Error"

        # Exibe o histórico de transações da primeira conta do cliente
        customer_obj = customer_obj.accounts[0]
        print("\n======= EXTRATO ========")
        customer_obj.history.show()
        print(f"\nSaldo atual: R$ {customer_obj.balance:.2f}")
        print("========================")

        return "Success"
