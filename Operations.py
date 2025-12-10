'''
    Define a interface de operações para o cliente.
''' 

import server.consts as consts
import server.utils as utils
from exceptions import RpcServerNotFound 

import socket
from datetime import datetime
import json
import functools  # Requerido por wraps


# Dicionário simples para simular cache em memória principal
cache = {} # cache[key] = (resultado, timestamp)

# Configurações de conexão 
TIME_LIMIT = utils.get_limit_time()  # Retorna o tempo limite para armazenar o cache de noícias.


def use_cache(expire_minutes=None):
    ''' 
        Decorator Factory para cache em memória no cliente RPC. Com expiração opcional e fallback offline. 
    '''
    # Recebe a função a ser decorada (func) e retorna o wrapper
    def decorator(func):
        # Preserva metadados da função original (nome, docstring) quando a substituímos pelo wrapper 
        @functools.wraps(func)
        # Substituição temporária que pode executar código antes e/ou depois de chamar a função original
        def wrapper(*args, **kwargs):
            # Gera chave única serializada em JSON
            key = json.dumps( {'f': func.__name__, 'a': args, 'k': kwargs}, default=str, sort_keys=True)
            
            # Captura o timestamp atual
            now = datetime.now()

            # Verifica cache existente e validade (atribui o resultado à variável item e ao mesmo tempo avalia se o valor é verdadeiro)
            if (item := cache.get(key)):
                result, ts = item
                # Compara o tempo atual com o timestamp do cache
                time_diff = (now - ts).total_seconds()
                
                if not expire_minutes or time_diff < expire_minutes * 60:
                    print('Pegou do cache')
                    return result

            try:
                # Executa a operação normalmente
                result = func(*args, **kwargs)
                cache[key] = (result, now)
                return result
            except RpcServerNotFound:
                # Se servidor estiver offline, retorna o cache se existir
                if key in cache:
                    print('Servidor offline, usando cache')
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
        Returns: 
            str: Resultado da operação solicitada em string. 
    '''
    def __init__(self, ip: str, port: str):
        self.ip = ip
        self.port = port

    def execute(self, operation: str, *args: list[str]) -> str:
        '''
            Monta a operação para ser enviada ao servidor TCP.

            Args:
                operation (str): Tipo de operação (ex: 'sum', 'sub', 'div', etc).
                *args (str): Argumentos numéricos da operação.
            Returns: 
                str: Resultado retornado pelo servidor.
        '''
        # Monta a mensagem no formato esperado
        if args and len(args) > 0:
            message = f'{operation}\n' + '\n'.join(str(a) for a in args)
        else:
            message = operation

        try:
            # IP do client_server
            with utils.create_socket(self.ip, self.port, socket.SOCK_STREAM) as final_socket:                
                # Envia a operação codificada
                final_socket.sendall(message.encode())

                # Aguarda e retorna a resposta decodificada 
                return final_socket.recv(4096).decode()
            
        except (socket.error, ConnectionRefusedError) as e:
            raise RpcServerNotFound(f'Erro ao conectar no client_server: {e}')


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
    
    @use_cache()
    def check_primes(self, *numbers: list[str]) -> list[str]:
        return self.execute(consts.PRIME, *numbers)

    @use_cache(expire_minutes=5)
    def get_uol_news(self) -> str:
        return self.execute(consts.NEWS)
