# Define a interface de operações para o cliente.

import tcp_client as client
import server.consts as consts
from exceptions import RpcServerNotFound 
import functools  # Usado para wraps
import time       # Usado para timestamp

# Dicionário simples para simular cache em memória principal
cache = {} # cache[key] = (resultado, timestamp)

import functools
import time
import json
from exceptions import RpcServerNotFound

cache = {}

def use_cache(expire_minutes=None):
    """ 
    Decorator Factory para cache em memória no cliente RPC. Com expiração opcional e fallback offline. 
    """
    # Recebe a função a ser decorada (func) e retorna o wrapper
    def decorator(func):
        # Preserva metadados da função original (nome, docstring) quando a substituímos pelo wrapper 
        @functools.wraps(func)
        # Substituição temporária que pode executar código antes e/ou depois de chamar a função original
        def wrapper(*args, **kwargs):
            # Gera chave única serializada em JSON
            key = json.dumps( {"f": func.__name__, "a": args, "k": kwargs}, default=str, sort_keys=True)
            now = time.time()

            # Verifica cache existente e validade (atribui o resultado à variável item e ao mesmo tempo avalia se o valor é verdadeiro)
            if (item := cache.get(key)):
                result, ts = item
                if not expire_minutes or now - ts < expire_minutes * 60:
                    print("Pegou do cache")
                    return result

            try:
                # Executa a operação normalmente
                result = func(*args, **kwargs)
                cache[key] = (result, now)
                return result
            except RpcServerNotFound:
                # Se servidor estiver offline, retorna o cache se existir
                if key in cache:
                    print("Servidor offline — usando cache")
                    return cache[key][0] 
                raise # senão, relança o erro
        return wrapper
    return decorator

class Operations:
    '''
    Classe responsável por enviar requisições de operações matemáticas para o servidor via socket TCP.
    Constroi a mensagem no formato esperado pelo servidor. Formato de mensagem: <OPERAÇÃO>\n<ARG1>\n<ARG2>\n...

    Args:
        ip (str): Endereço IP do servidor.
        port (int): Porta TCP do servidor.
    Returns: Resultado da operação solicitada em string. 
    '''
    def __init__(self, ip: str, port: str):
        self.ip = ip
        self.port = port

    def execute(self, operation: str, *args: list[str]) -> str:
        """
        Monta a operação para ser enviada ao servidor TCP.

        Args:
            operation (str): Tipo de operação (ex: 'sum', 'sub', 'div', etc).
            *args (str): Argumentos numéricos da operação.
        Returns: str: Resultado retornado pelo servidor.
        """
        # Monta a mensagem no formato esperado
        if args and len(args) > 0:
            message = f"{operation}\n" + "\n".join(str(a) for a in args)
        else:
            message = operation
        return client.execute_remote_operation(self.ip, self.port, message)

    @use_cache()
    def addition(self, *numbers: list[str]) -> str:
        return self.execute(consts.SUM, *numbers)

    @use_cache()
    def subtraction(self, *numbers: list[str]) -> str:
        return self.execute(consts.SUB, *numbers)

    @use_cache()
    def multiplication(self, *numbers: list[str]) -> str:
        return self.execute(consts.MUL, *numbers)

    @use_cache()
    def division(self, *numbers: list[str]) -> str:
        return self.execute(consts.DIV, *numbers)

    @use_cache()
    def factorial(self, x: str) -> str:
        return self.execute(consts.FAC, x)

    @use_cache(expire_minutes=5)
    def get_uol_news(self) -> str:
        return self.execute(consts.NEWS)
