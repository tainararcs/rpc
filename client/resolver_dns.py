# É acessado pelo client_socket, retorna para ele o ip do servidor de operações (ou o servidor de cada operação)
# Ele que pergunta os ips

import server.utils as utils
import server.exceptions as excepts
import socket
import json 
import os

# Configurações para se conectar ao servidor de DNS autoritativo
IP = utils.get_ip_dns()       # Retorna '127.0.0.1'
PORT = utils.get_port_dns()   # Retorna 11111

CACHE_FILE = 'dns_cache.json'

def search_operation(operation: str) -> str:
    # Garante que o arquivo exista
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        return None
    else:
        cache = json.load(f)

    return cache.get(operation.strip())

def write_cache(operation: str, ip: str, port: int) -> None:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
    else:
        cache = {}

    cache[operation] = {'ip': ip, 'port': port}

    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=4)

def lookup_service(operation: str) -> str: 
    '''
        Consulta o servidor DNS autoritativo para obter o endereço IP e a porta do servidor responsável por uma operação.

        Args:
            operation (str): Nome da operação (ex: 'math', 'news').
    '''
    operation = operation.lower()
    cached = search_operation(operation)

    # Verifica se a operação está em cache
    if cached:
        print(f'\nOperação {operation} já disponível em cache')
        return cached['ip'], cached['port']
    
    # Consulta DNS autoritativo via UDP
    try: 
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as resolver_socket:
            # Define timeout para evitar bloqueio infinito
            resolver_socket.settimeout(5)

            # Envia a operação para o servidor DNS
            resolver_socket.sendto(operation.lower().encode(), (IP, PORT))
            
            # Recebe a resposta do servidor DNS
            data, _ = resolver_socket.recvfrom(4096)

            response = json.loads(data.decode())

            if 'error' in response:
                raise excepts.OperationNotFound(f'Operação "{operation}" não encontrada no DNS ({IP}:{PORT})') 

            return response['ip'], response['port']

    except socket.timeout:
        raise excepts.RpcServerNotFound(f'\nTimeout ao conectar no DNS ({IP}:{PORT})')
    except Exception as e:
        raise excepts.RpcServerNotFound(f'\nErro no servidor Resolver DNS ({IP}:{PORT})\n\n{e}')
    except KeyboardInterrupt:
        print('\n\nDNS resolver encerrado pelo usuário (CTRL+C)')
    finally:
        print('Servidor Finalizando...\n')
        