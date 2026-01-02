'''
'''

import server.consts as consts
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
