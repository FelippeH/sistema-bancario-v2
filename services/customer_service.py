from models.customer import Individual


# Classe que representa o serviço de gerenciamento de clientes
class CustomerService:
    def __init__(self):
        self.service_customers = []

    # Método para encontrar um cliente pelo CPF
    # utilizo esse método apenas no create_user
    def find_by_cpf_only(self, cpf):
        for c in self.service_customers:
            if isinstance(c, Individual) and c.cpf == cpf:
                return c
        return None

    # Método para encontrar um cliente pelo CPF e senha
    # utilizo esse método apenas no create_checking_account
    def find_by_cpf_and_password(self, cpf, password):
        for c in self.service_customers:
            if isinstance(c, Individual) and c.cpf == cpf and c.password == password:
                return c
        return None

    # Método para encontrar um cliente apenas pela senha
    # utilizo esse método para solicitar o depósito, saque e exibir extrato.
    def find_by_password_only(self, password):
        for c in self.service_customers:
            if isinstance(c, Individual) and c.password == password:
                return c
        return None

    # Método para adicionar um novo cliente
    def add_customer(self, customer):
        self.service_customers.append(customer)
