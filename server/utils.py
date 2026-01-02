'''
    Módulo de utilidades do sistema RPC.
    Fornece funções auxiliares para leitura de configurações a partir do arquivo JSON central da aplicação.
'''

import json
import server.consts as consts


#  Configurações do cliente
def get_ip_client() -> str:
    '''
        Retorna o endereço IP do servidor cliente (gateway).

        Returns:
            str: Endereço IP configurado.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('ip-client')

def get_port_client() -> int:
    '''
        Retorna a porta TCP do servidor cliente (gateway).

        Returns:
            int: Porta configurada.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return int(config.get('port-client'))


# Configurações do servidor de operações
def get_ip_operations() -> str:
    '''
        Retorna o endereço IP do servidor de operações.

        Returns:
            str: Endereço IP configurado.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('ip-operations')


def get_port_operations() -> int:
    '''
        Retorna a porta TCP do servidor de operações.

        Returns:
            int: Porta configurada.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return int(config.get('port-operations'))


# Configurações do DNS
def get_ip_dns() -> str:
    '''
        Retorna o endereço IP do DNS autoritativo.

        Returns:
            str: Endereço IP configurado.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('ip-dns')


def get_port_dns() -> int:
    '''
        Retorna a porta do DNS autoritativo.

        Returns:
            int: Porta configurada.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return int(config.get('port-dns'))


# Configurações gerais
def get_cache_size() -> int:
    '''
        Retorna o tamanho máximo permitido para o cache em disco.

        Returns:
            int: Tamanho do cache em bytes.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('cache-size')


def get_limit_time() -> int:
    '''
        Retorna o tempo limite de validade do cache em memória.

        Returns:
            int: Tempo limite em minutos.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('limit-time')
