'''
    Módulo de utilidades do sistema RPC.
    Fornece funções auxiliares para leitura de configurações a partir do arquivo JSON central da aplicação.
'''

import server.consts as consts
import json

#  Configurações do cliente
def get_ip_client_server() -> str:
    '''
        Retorna o endereço IP do servidor cliente (gateway).

        Returns:
            str: Endereço IP configurado.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('ip-client-server')

def get_port_client_server() -> int:
    '''
        Retorna a porta TCP do servidor cliente (gateway).

        Returns:
            int: Porta configurada.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return int(config.get('port-client-server'))


# Configurações do servidor de operações
def get_ip_math_server() -> str:
    '''
        Retorna o endereço IP do servidor de operações.

        Returns:
            str: Endereço IP configurado.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('ip-math-server')


def get_port_math_server() -> int: 
    '''
        Retorna a porta TCP do servidor de operações.

        Returns:
            int: Porta configurada.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return int(config.get('port-math-server'))

def get_ip_news_server() -> str:
    '''
        Retorna o endereço IP do servidor de operações.

        Returns:
            str: Endereço IP configurado.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('ip-news-server')


def get_port_news_server() -> int: 
    '''
        Retorna a porta TCP do servidor de operações.

        Returns:
            int: Porta configurada.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return int(config.get('port-news-server'))

def get_ip_ia_server() -> str:
    '''
        Retorna o endereço IP do servidor de operações.

        Returns:
            str: Endereço IP configurado.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('ip-ia-server')


def get_port_ia_server() -> int: 
    '''
        Retorna a porta TCP do servidor de operações.

        Returns:
            int: Porta configurada.
    '''
    with open(consts.CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return int(config.get('port-ia-server'))

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
