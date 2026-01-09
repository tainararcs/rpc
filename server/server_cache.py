'''
    Módulo de cache persistente em disco para operações do servidor.
    Permite armazenar e recuperar resultados de operações, com controle de tamanho máximo do cache.
'''

import server.utils as utils
from collections import OrderedDict
import os
import json

CACHE_FILE = 'server/operations_cache.json'
MAX_CACHE_BYTES = utils.get_cache_size()  # Retorna o limite de bytes do cache em disco

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