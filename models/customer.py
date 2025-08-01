# classe base que representa um cliente genérico
class Customer:
    def __init__(self, address):
        self.address = address # endereço do cliente
        self.accounts = [] # lista de contas associadas ao cliente
        
    def make_transactions(self, transaction):
        # executa uma transação em uma conta
        # verifica se o cliente possui contas
        if not self.accounts:
            print("\n❌ Este cliente não possui contas.")
            return False
    
        # realiza a transação na primeira conta do cliente
        return self.accounts[0].make_transaction(transaction)
        
    def add_account(self, account):
        # adiciona uma nova conta à lista de contas do cliente
        self.accounts.append(account)
        
# classe que representa um cliente pessoa física, herda de customer
class Individual(Customer):
    def __init__(self, cpf, name, address):
        super().__init__(address) # chama o construtor da superclasse customer para inicializar o endereço
        self.cpf = cpf
        self.name = name