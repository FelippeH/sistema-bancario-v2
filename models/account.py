from models.transaction import Withdrawal
from models.history import History
from datetime import date

# decorador para limitar o número de transações diárias
def transaction_limit(max_transactions):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            today = date.today()

            todays_transactions = [
                t for t in self.history._transactions if t.date.date() == today
            ] # filtra as transações do dia

            # verifica se o número de transações diárias atingiu o limite
            if len(todays_transactions) >= max_transactions:
                return "daily_transactions_limit_exceeded"
            
            # chama a função original se o limite não foi atingido
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

# classe que representa uma conta bancária.
class Account:
    def __init__(self, number, customer):
        self._balance = 0
        self._agency = "001" # número da agência bancária. O número começa em '001', e é atribuído um novo número para cada conta criada.
        self._number = number # número da conta corrente.
        self._customer = customer # cliente dono da conta.
        self._history = History() # histórico de transações da conta.
       
    # propriedades para acessar atributos privados.
    # uso do @property para modo apenas leitura.
    @property 
    def balance(self):
        return self._balance
    
    @property
    def agency(self):
        return self._agency
    
    @property
    def number(self):
        return self._number
    
    @property
    def customer(self):
        return self._customer
    
    @property
    def history(self):
        return self._history
    
    # método de classe para criar uma nova conta, facilitando a instanciação
    @classmethod
    def new_account(cls, customer, number):
        return cls(number, customer)
    
    @transaction_limit(max_transactions=15) # decorador para limitar transações diárias
    def make_transaction(self, transaction):
        return transaction.register(self)
    
    # método para realizar saque
    def withdrawal(self, value):
        # Verifica se o valor do saque é positivo
        if value > self._balance:
            return False
        
        self._balance -= value
        return True
            
    # método para realizar depósito
    def deposit(self, value):
        
        # Verifica se o valor do depósito é maior que o limite
        if value > 2500:
            return False
            
        # Verifica se o valor do depósito é positivo
        elif value > 0:
            self._balance += value
            return True
            
        else:
            return False
        
# criação da conta corrente com verificação de limite de quantidade de saques e limite de valor permitido por saque.
# classe que herda da classe Account, representando uma conta corrente.
class CheckingAccount(Account):
    def __init__(self, number, customer, limit=2000, withdrawal_limit=5):
        super().__init__(number, customer)
        self._limit = limit
        self._withdrawal_limit = withdrawal_limit

    # método para realizar saque com verificação de limite de valor e quantidade de saques.
    def withdrawal(self, value):
        num_withdrawals = len([
            transaction for transaction in self.history._transactions
        if isinstance(transaction, Withdrawal)])

        # Verifica se o valor do saque é maior que o limite
        if value > self._limit:
            return "limit_exceeded"
        
        # verifica se o número de saques diários atingiu o limite
        if num_withdrawals >= self._withdrawal_limit:
            return "withdrawal_exceeded"

        # Verifica se há saldo suficiente na conta
        success = super().withdrawal(value)
        if not success:
            return "insufficient_funds"

        return True