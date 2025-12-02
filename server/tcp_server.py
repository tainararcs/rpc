# Socket servidor

import os
import socket
import json

import consts as consts
import math_operations as math
from collections import OrderedDict
 
CACHE_FILE = 'cache.json'


# Lê o arquivo de configurações
with open('configuracoes.txt', 'r') as f:
    config = json.load(f)

# Configurações de conexão 
HOST = config.get('ip')  # Retorna '127.0.0.1'
PORT = config.get('port')  # Retorna 11100
MAX_CACHE_BYTES = config.get("limite-size") # Retorna o limite de bytes do cache em disco

# Recebe a operação enviada pelo cliente e chama a função correspondente à operação
def manage_request(parts_data: str) -> str:
    """
    Recebe a lista com a operação e os parâmetros e executa a função correspondente.

    Args: parts_data (list[str]): Lista onde o primeiro elemento é a operação e os seguintes são os argumentos.
    Returns: str: Resultado da operação.
    """
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
            return math.factorial(parts_data[1])
        case consts.NEWS:
            return math.get_uol_news()
        case _:
            return "Operação inválida"

def search_operation(operation: str) -> str | None:
    """
    Pesquisa se uma operação já foi executada e armazenada no cache.

    Args: operation (str): Representação textual da operação (ex: "sum 2 3").
    Returns: str | None: Resultado armazenado, ou None se não estiver no cache.
    """
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
    # Lê o cache existente, se existir
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            try:
                cache = json.load(f, object_pairs_hook=OrderedDict)
                print(f"Cache lido antes de adicionar: {cache}")
            except json.JSONDecodeError:
                cache = OrderedDict()
    else:
        cache = OrderedDict()

    # Adiciona a nova operação ao cache
    print(f"Adicionando operação ao cache: {operation}")
    cache[operation] = result

    # Verifica o tamanho do cache antes da remoção
    cache_size = len(json.dumps(cache).encode())
    print(f"Tamanho do cache antes da remoção: {cache_size} bytes")
    
    # Remove itens antigos até que o tamanho do cache seja aceitável
    while cache_size + len(result.encode()) > MAX_CACHE_BYTES and len(cache) > 1:
        print(f"Removendo um item do cache. Tamanho atual: {cache_size} bytes")
        cache.popitem(last=False)  # Remove o item mais antigo
        cache_size = len(json.dumps(cache).encode())  # Atualiza o tamanho do cache

    print(f"Tamanho do cache após a remoção: {cache_size} bytes")

    # Verifica se o cache tem tamanho válido para ser gravado
    if (cache_size + len(result)) < MAX_CACHE_BYTES:
        with open(CACHE_FILE, 'w') as f:
            print('Gravando cache no arquivo...')
            json.dump(cache, f, indent=4)
        print(f"Cache gravado com sucesso: {cache}")
    else:
        print("Cache excedeu o tamanho limite, não foi possível gravar")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    
    # Espera no máximo 30 segundos por conexão
    server_socket.settimeout(100)  
    print(f"\nServidor ouvindo em {HOST}:{PORT}")

    while True:
        try:
            connection, address = server_socket.accept()
        except socket.timeout:
            print("\nNenhuma conexão recebida, encerrando servidor...\n")
            break  # Sai do loop e encerra o servidor

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
            