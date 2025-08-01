from abc import ABC, abstractmethod
from datetime import datetime

# Esta classe Transaction não está sendo usada para saques, mas vou manter para contexto
class Transaction(ABC):
    def __init__(self, value, date=None):
        if value <= 0:
            raise ValueError("\n❌ O valor da transação deve ser positivo.")
        self._value = value
        self.date = date if date else datetime.now()

    @property
    def value(self):
        return self._value
    
    @abstractmethod
    def register(self, account):
        pass

# classe que representa um depósito, herda de transaction
class Deposit(Transaction):
    def register(self, account):
        # Captura o resultado da chamada ao método deposito da conta
        if account.deposit(self.value):
            account.history.add_transaction(self)
            return True
        return False

# classe que representa um saque, herda de transaction
class Withdrawal(Transaction):
    def register(self, account):
        # Captura o resultado da chamada ao método withdrawal da conta
        result = account.withdrawal(self.value)
        
        # Se o resultado for True, o saque foi bem-sucedido
        if result is True:
            account.history.add_transaction(self)
            return True
        else:
            # Caso contrário, retorna a string de erro
            return result