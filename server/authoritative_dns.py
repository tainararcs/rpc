'''
    Servidor DNS Autoritativo do sistema RPC.
    Mantém a tabela oficial de mapeamento entre operações e servidores responsáveis. 
    Responde a consultas DNS via UDP, retornando o IP e a porta do servidor que implementa a operação solicitada.
'''
import server.utils as utils
import server.exceptions as excepts
import json
import socket

# Configurações para se conectar com o DNS resolver
IP = utils.get_ip_dns()      # Retorna '127.0.0.1'
PORT = utils.get_port_dns()  # Retorna 11112

DNS_TABLE = 'server/dns_table.json'

def load_dns_table() -> dict:
    ''' 
        Carrega a tabela DNS do arquivo JSON.

        Returns:
            dict: Estrutura contendo operações como chave e dados do servidor como valor.
    '''
    with open(DNS_TABLE, 'r') as f:
        return json.load(f)

def get_operation_server_ip(operation: str) -> tuple[str, int]:
    '''
        Obtém o IP e a porta do servidor responsável por uma operação.

        Args:
            operation (str): Nome da operação solicitada.
        Returns:
            tuple[str, int] | None: Tupla com IP e porta do servidor, ou None se não encontrado.
    '''
    table = load_dns_table()
    entry = table.get(operation.lower())

    if entry:
        return entry.get('ip'), entry.get('port')

    return None

try: 
    # Cria o socket UDP do DNS autoritativo
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((IP, PORT))
        print(f'\nDNS autoritativo ouvindo em {IP}:{PORT}')

        while True:
            # Recebe consulta do resolver
            data, address = server_socket.recvfrom(4096)
            data = data.decode().lower()
            
            if not data:
                continue

            print('Operação recebida no DNS autoriatativo: ', data)
            response = get_operation_server_ip(data)

            # Monta payload para evitar enviar tupla
            if response:
                payload = json.dumps({'ip': response[0], 'port': response[1]})
            else:
                payload = json.dumps({'error': 'operacao nao encontrada'})

            server_socket.sendto(str(payload).encode(), address)

except (socket.error, ConnectionRefusedError) as e:
    raise excepts.RpcServerNotFound(f'\nErro no servidor Authoritative DNS\n\n{e})')
except KeyboardInterrupt:
    print('\n\nDNS authoritative encerrado pelo usuário (CTRL+C)')
finally:
    print('Servidor Finalizando...\n')
    