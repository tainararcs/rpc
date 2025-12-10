'''
    Socket cliente. Gateway
''' 

import server.utils as utils
import resolver_dns as resolver_dns

import socket
import exceptions

# Informações para se conectar ao servidor de DNS
IP = utils.get_ip_client()       # Retorna '127.0.0.1'
PORT = utils.get_port_client()   # Retorna 11110

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Para operations se conectar ao cliente_server
    client_socket.bind((IP, PORT))
    client_socket.listen()
    print(f'\nServidor cliente ouvindo em {IP}:{PORT}')

    while True:
        try:
            connection, address = client_socket.accept()

            with connection:
                data = connection.recv(4096).decode().lower()
                if not data:
                    continue

                # Extrai apenas a operação (primeira linha)
                operation = data.split('\n')[0]

                # Descobre o serviço de operações pelo DNS (passa apenas a operação)
                ip, port = resolver_dns.lookup_service(operation)
                print(f'DNS autoritativo retornou: {ip}:{port} para "{operation}"')

                # Conecta no servidor final
                with utils.create_socket(ip, port, socket.SOCK_STREAM) as final_socket:
                    # Envia a mensagem completa (operação + argumentos)
                    final_socket.sendall(data.encode())

                    # Aguarda e retorna a resposta decodificada 
                    response = final_socket.recv(4096).decode()
                
                # Envia a resposta de volta para o client_server
                connection.sendall(str(response).encode())

        except (socket.error, ConnectionRefusedError) as e:
            raise exceptions.RpcServerNotFound(f'Erro no servidor cliente:\n\n{e}')
        except KeyboardInterrupt:
            print('\n\nServidor cliente encerrado pelo usuário (CTRL+C)')
        finally:
            print('Servidor Finalizando...\n')