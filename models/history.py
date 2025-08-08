from models.transaction import Transaction


# classe para armazenar o histórico de transações da conta
class History:
    def __init__(self):
        # lista privada para guardar transações
        self._transactions = []

    def add_transaction(self, transaction):
        # adiciona uma nova transação ao histórico
        if not isinstance(transaction, Transaction):
            raise TypeError("Transação inválida.")
        self._transactions.append(transaction)

    # método para exibir o histórico de transações
    def show(self):

        # mapeia os nomes das transações para exibição no terminal
        TRANSACTION_NAMES = {"Deposit": "Depósito", "Withdrawal": "Saque"}
        # mostra todas as transações feitas na conta
        for index, t in enumerate(self._transactions, start=1):

            # formata a data da transação para exibição
            date_str = t.date.strftime("%d/%m/%Y às %H:%M:%S")
            name_pt = TRANSACTION_NAMES.get(t.__class__.__name__, __class__.__name__)
            print(f"{index}. {name_pt} de R$ {t.value:.2f} efetuado em {date_str}")
