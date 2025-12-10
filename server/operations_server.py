'''
    Socket servidor.
''' 

import server.consts as consts
import server.utils as utils
import server.math_operations as math
import server.general_operations as general
import exceptions

from collections import OrderedDict
import os
import socket
import json


CACHE_FILE = 'server/operations_cache.json'

# Configurações de conexão 
IP = utils.get_ip_operations()        # Retorna '127.0.0.1'
PORT = utils.get_port_operations()    # Retorna 11111

MAX_CACHE_BYTES = utils.get_cache_size() # Retorna o limite de bytes do cache em disco


# Recebe a operação enviada pelo cliente e chama a função correspondente à operação
def manage_request(parts_data: str) -> str:
    '''
        Recebe a lista com a operação e os parâmetros e executa a função correspondente.

        Args: 
            parts_data (list[str]): Lista onde o primeiro elemento é a operação e os seguintes são os argumentos.
        Returns: 
            str: Resultado da operação.
    '''
    operation = parts_data[0].lower()
    match operation:
        case consts.SUM:
            return math.addition(parts_data[1:])
        case consts.SUB:
            return math.subtraction(parts_data[1:])
        case consts.MUL:
            return math.multiplication(parts_data[1:])
        case consts.DIV:
            return math.division(parts_data[1:])
        case consts.FAC:
            return math.factorial(parts_data[1])  # Envia apenas o número
        case consts.PRIME:
            return math.check_primes(parts_data[1:])
        case consts.NEWS:
            return general.get_uol_news()
        case _:
            return 'Operação inválida'

def search_operation(operation: str) -> str | None:
    '''
        Pesquisa uma operação no cache.

        Args:
            operation (str): Representação textual da operação (ex: 'sum 2 3').
        Returns: 
            str | None: Resultado da operação se encontrada, ou None.
    '''
    # Garante que o arquivo exista
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'w') as f:
            json.dump({}, f)
            return None

    with open(CACHE_FILE, 'r') as f:
        try:
            cache = json.load(f)
        except json.JSONDecodeError:
            cache = {}

    return cache.get(operation.strip())

def write_cache(operation: str, result: str) -> None:
    '''
        Grava o resultado de uma operação no cache, respeitando o limite de tamanho.

        Args: 
            operation (str): Representação textual da operação (ex: 'sum 2 3').
            result (str): Resultado da operação a ser armazenado.
    '''
    # Lê o cache existente, se existir
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            try:
                cache = json.load(f, object_pairs_hook=OrderedDict)
            except json.JSONDecodeError:
                cache = OrderedDict()
    else:
        cache = OrderedDict()

    # Adiciona a nova operação ao cache
    print(f'Adicionando operação ao cache: {operation}')
    cache[operation] = result

    # Verifica o tamanho do cache antes da remoção
    cache_size = len(json.dumps(cache).encode())
    
    # Remove itens antigos até que o tamanho do cache seja aceitável
    while cache_size + len(result.encode()) > MAX_CACHE_BYTES and len(cache) > 1:
        print(f'Removendo um item do cache. Tamanho atual: {cache_size} bytes')
        cache.popitem(last=False)  # Remove o item mais antigo
        cache_size = len(json.dumps(cache).encode())  # Atualiza o tamanho do cache


    # Verifica se o cache tem tamanho válido para ser gravado
    if (cache_size + len(result)) < MAX_CACHE_BYTES:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=4)
    else:
        print('Cache excedeu o tamanho limite, não foi possível gravar')

# Será q da pra usar utils.create_connection aqui?
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as operations_socket:
    operations_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    operations_socket.bind((IP, PORT))
    operations_socket.listen()
    print(f'\nServidor ouvindo em {IP}:{PORT}')

    # Espera no máximo 30 segundos por conexão
    operations_socket.settimeout(100)  
    
    try:
        while True:
            connection, address = operations_socket.accept()
            print(f'Conectado com {address}')

            with connection:
                data = connection.recv(4096).decode().lower()
                if not data:
                    continue
                
                # Envia os parâmetros da requisição para serem pesquisados no cache
                cache = search_operation(data)
                if cache:
                    print('\nPegou do cache')
                    response = cache
                else:  
                    response = manage_request(data.strip().split('\n'))
                    write_cache(data, str(response))

                connection.sendall(str(response).encode())

    except (socket.error, ConnectionRefusedError) as e:
        raise exceptions.RpcServerNotFound(f'Erro no servidor de operações:\n\n{e}')
    except KeyboardInterrupt:
        print('\n\nServidor de operações encerrado pelo usuário (CTRL+C)')
    finally:
        print('Servidor Finalizando...\n')