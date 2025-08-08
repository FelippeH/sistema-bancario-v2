from datetime import datetime
from pathlib import Path
import sys

# define o caminho raiz do projeto
ROOT_PATH = Path(__file__).parent.parent
sys.path.append(str(ROOT_PATH / ''))

# decorador para registrar transações no log.txt
def transaction_log(func):
    def envelope(*args, **kwargs):
        result = func(*args, **kwargs)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # registra a transação no log.txt
        with open(ROOT_PATH / "log.txt", "a", newline= "", encoding="utf-8") as archive:
            archive.write(f"[{now}] Function {func.__name__} executed with arguments {args[-1]}, {kwargs}. "
                          f"Return {result}\n")
        return result
    return envelope