# Tem acesso a lista e retorna um json com as possibilidades de operações (um ip pra cada operação?)
# Ele quem responde

import server.utils as utils
import exceptions as excepts

import json
import socket
import datetime


# Configurações para se conectar com o DNS resolver
IP = utils.get_ip_dns()      # Retorna '127.0.0.1'
PORT = utils.get_port_dns()  # Retorna 1111

DNS_TABLE = 'server/dns_table.json'


def load_dns_table():
    with open(DNS_TABLE, 'r') as f:
        return json.load(f)

def get_operation_server_ip(operation: str):
    table = load_dns_table()
    entry = table.get(operation.lower())

    if entry:
        return entry.get('ip'), entry.get('port')

    return None

try: 
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((IP, PORT))
        print(f'\nDNS autoritativo ouvindo em {IP}:{PORT}')

        while True:
            data, address = server_socket.recvfrom(4096)
            data = data.decode().lower()
            
            if not data:
                continue

            print('Recebido no DNS:', data)

            response = get_operation_server_ip(data)

            # Evitar enviar tupla
            if response:
                payload = json.dumps({'ip': response[0], 'port': response[1]})
            else:
                payload = json.dumps({'error': 'operacao nao encontrada'})

            server_socket.sendto(str(payload).encode(), address)

except (socket.error, ConnectionRefusedError) as e:
    raise excepts.RpcServerNotFound(f'Erro no servidor Authoritative DNS\n\n{e})')
except KeyboardInterrupt:
    print('\n\nDNS authoritative encerrado pelo usuário (CTRL+C)')
finally:
    print('Servidor Finalizando...\n')