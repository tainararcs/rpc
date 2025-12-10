'''
'''

import server.consts as consts

import socket
import json

# Servidor cliente
def get_ip_client() -> str:
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('ip-client')
    
def get_port_client() -> int:
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return int(config.get('port-client'))

# Servidor de operações
def get_ip_operations() -> str:
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('ip-operations')
    
def get_port_operations() -> int:
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return int(config.get('port-operations'))
    
# DNS
def get_ip_dns() -> str:
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('ip-dns')
    
def get_port_dns() -> int:
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return int(config.get('port-dns'))

# Gerais
def get_cache_size() -> str:
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('cache-size')

def get_limit_time() -> str:
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('limit-time')
    

def create_socket(host: str, port: str, type_connection: socket) -> socket.socket:
    '''
        Cria e retorna um socket TCP ou UDP conectado ao servidor especificado.

        Args:
            host (str): Endereço IP do servidor.
            port (int): Porta TCP do servidor.
        Returns: 
            socket.socket: Socket TCP ou UDP conectado ao servidor.
    '''
    new_socket = socket.socket(socket.AF_INET, type_connection)
    new_socket.connect((host, port))
    return new_socket
