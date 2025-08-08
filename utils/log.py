import inspect
from datetime import datetime
from pathlib import Path

# define o caminho raiz do projeto
UTILS_PATH = Path(__file__).parent.resolve()
LOG_FILE = UTILS_PATH / "log.txt"


# decorador para registrar transações no log.txt
def transaction_log(func):
    def envelope(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        # OrderedDict com {nome_param: valor}
        arguments = bound.arguments
        cpf = arguments.get("cpf", None)
        name = arguments.get("name", None)
        address = arguments.get("address", None)
        value = arguments.get("value", None)

        result = func(*args, **kwargs)

        # Registra a transação no log
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as archive:
            archive.write(
                f"[{now}] Function {func.__name__} executed."
                f"\nCPF: {cpf},"
                f"\nName: {name},"
                f"\nAddress: {address},"
                f"\nValue: {value},"
                f"\nReturn: {result}\n\n"
            )
        return result

    return envelope
