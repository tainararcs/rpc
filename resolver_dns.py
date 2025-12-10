# É acessado pelo client_socket, retorna para ele o ip do servidor de operações (ou o servidor de cada operação)
# Ele que pergunta os ips

import server.utils as utils
import exceptions as excepts

import socket
import json 
import datetime


# Configurações para se conectar ao servidor de DNS autoritativo
IP = utils.get_ip_dns()       # Retorna '127.0.0.1'
PORT = utils.get_port_dns()   # Retorna 11111

CACHE_FILE = 'dns_cache.json'


def load_cache():
    pass

def save_cache(cache):
    pass

def lookup_service(operation: str) -> str: 
    '''
        Consulta o servidor DNS autoritativo para obter o endereço IP e a porta do servidor responsável por uma operação.

        Args:
            operation (str): Nome da operação (ex: 'math', 'news').
    '''

    # Verifica se a operação está no cache
    
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
                raise excepts.RpcServerNotFound(f'Operação "{operation}" não encontrada no DNS ({IP}:{PORT})') # Trocar exceção

            return response['ip'], response['port']

    except socket.timeout:
        raise excepts.RpcServerNotFound(f'Timeout ao conectar no DNS ({IP}:{PORT})')
    except Exception as e:
        raise excepts.RpcServerNotFound(f'Erro no servidor Resolver DNS ({IP}:{PORT})\n\n{e}')
    except KeyboardInterrupt:
        print('\n\nDNS resolver encerrado pelo usuário (CTRL+C)')
    finally:
        print('Servidor Finalizando...\n')