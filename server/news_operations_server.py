'''
    Servidor de Operações do sistema RPC.
    Recebe requisições TCP contendo operações e parâmetros, executa a função correspondente e retorna o resultado ao cliente.
    Inclui um cache persistente em disco com controle de tamanho máximo.
''' 

import server.consts as consts
import server.utils as utils
import server.general_operations_service as general
import server.exceptions as excepts
from collections import OrderedDict
import os
import socket
import json

CACHE_FILE = 'server/operations_cache.json'

# Configurações de conexão 
IP = utils.get_ip_news_server()        # Retorna '127.0.0.1'
PORT = utils.get_port_news_server()    # Retorna 11112

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
        Armazena o resultado de uma operação no cache, respeitando o limite de tamanho.
        - FIFO (remove operações mais antigas primeiro).
        
        Args: 
            operation (str): Representação textual da operação (ex: 'sum 2 3').
            result (str): Resultado da operação a ser armazenado.
    '''
    # Lê o cache existente
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            try:
                cache = json.load(f, object_pairs_hook=OrderedDict)
            except json.JSONDecodeError:
                cache = OrderedDict()
    else:
        cache = OrderedDict()

    # Adiciona a nova operação ao cache
    print(f'Operação adicionada ao cache: {operation!r}')
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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as operations_socket:
    operations_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    operations_socket.bind((IP, PORT))
    operations_socket.listen()
    print(f'\nServidor de notícias ouvindo em {IP}:{PORT}')
    
    try:
        while True:
            connection, address = operations_socket.accept()
            print(f'Conectado com {address}\n')

            with connection:
                data = connection.recv(4096).decode().lower()
                if not data:
                    continue
                
                # Envia os parâmetros da requisição para serem pesquisados no cache
                cache = search_operation(data)
                if cache:
                    print('\nOperação já disponível em cache')
                    response = cache
                else:  
                    response = manage_request(data.strip().split('\n'))
                    write_cache(data, str(response))

                connection.sendall(str(response).encode())

    except (socket.error, ConnectionRefusedError) as e:
        raise excepts.RpcServerNotFound(f'\nErro no servidor de operações:\n\n{e}')
    except KeyboardInterrupt:
        print('\n\nServidor de operações encerrado pelo usuário (CTRL+C)')
    finally:
        print('Servidor Finalizando...\n')
        