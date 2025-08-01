## Sistema Bancário em Python – Versão 2.0

Esta é a segunda versão do projeto de sistema bancário desenvolvido em python, com foco em aprimoramento estrutural e boas práticas de programação.

### **Objetivo:**

Desenvolver um sistema bancário funcional que permita ao usuário realizar operações como criação de contas, cadastro de usuários, saques, depósitos, consulta de extrato, entre outras funcionalidades listadas na seção "Funcionalidades".

Nesta nova versão, o projeto foi reestruturado com base nos princípios da Programação Orientada a Objetos (POO), promovendo:
- _Melhor organização do código, com separação clara de responsabilidades._
- _Encapsulamento, garantindo maior segurança e integridade dos dados._
- _Reutilização de classes e métodos, facilitando a manutenção e a expansão futura do sistema._

# Funcionalidades:

- Criar usuário
- Criar conta corrente
- Listar contas
- Fazer depósitos
- Fazer saques
- Consultar o extrato

# Estruturação:

As classes são divididas em arquivos separados, à fim de manter uma melhor organização do projeto, e são dividos em account, customer, history e transaction.

## Models:

### - init.py
Permite importar o diretório models como um pacote, viabilizando o uso de from models import account e similares.

### - account.py:
O arquivo account.py define a classe Account dentro do sistema. É responsável por armazenar as informações de uma conta bancária, como número da conta, cliente vinculado e histórico de transações. Também implementa os métodos de saque, depósito e geração de extrato, centralizando a lógica de movimentações financeiras da aplicação.

### - customer.py
Este arquivo contém a definição da classe Customer, que representa o cliente do banco. A classe armazena dados do titular (como nome e CPF) e também pode agrupar contas relacionadas a um mesmo cliente. É útil para identificar e vincular clientes às suas respectivas contas bancárias.

### - history.py
history.py tem a função de adicionar, armazenar e mostrar as informações do histórico de transações do usuário.

### - transaction.py
Define classes relacionadas às transações financeiras realizadas na conta. Possui abstrações como a classe Transaction e especializações como Withdraw e Deposit. Cada transação encapsula um valor, data e o tipo de operação realizada, além de aplicar regras específicas para execução.

## Menu:
### - menu.py
O menu.py torna o sistema funcional para o usuário, permitindo que o mesmo navegue por um menu via terminal. Ele organiza as opções disponíveis, como cadastrar cliente, criar conta, fazer depósito ou saque, e visualizar extratos, tornando o sistema interativo e acessível por linha de comando.

### - main.py
Responsável por iniciar a aplicação. Importa os módulos necessários, exibe o menu ao usuário e inicia o fluxo principal do programa. Em projetos maiores, esse arquivo costuma ser o ponto de entrada para execução e testes da aplicação.
