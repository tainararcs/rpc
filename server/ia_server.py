'''
    Servidor de Operações do sistema RPC.
    Recebe requisições TCP contendo operações e parâmetros, executa a função correspondente e retorna o resultado ao cliente.
    Inclui um cache persistente em disco com controle de tamanho máximo.
''' 

import server.general_operations_service as general
import server.consts as consts
import server.utils as utils
import server.exceptions as excepts
import server.server_cache as cache
import socket

# Configurações de conexão 
IP = utils.get_ip_ia_server()        # Retorna '127.0.0.1'
PORT = utils.get_port_ia_server()    # Retorna 11113

# Recebe a operação enviada pelo cliente e chama a função correspondente à operação
def manage_request(parts_data: str) -> str:
    '''
        Recebe a lista com a operação e os parâmetros e executa a função correspondente.

        Args: 
            parts_data (list[str]): Lista onde o primeiro elemento é a operação e os seguintes são os argumentos.
        Returns: 
            str: Resultado da operação.
    '''
    operation = parts_data[0].lower()
    match operation:
        case consts.SOLVER:
            return general.math_problem_solver(parts_data[1:])
        case _:
            return 'Operação inválida'
        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as operations_socket:
    operations_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    operations_socket.bind((IP, PORT))
    operations_socket.listen()
    print(f'\nServidor de ia ouvindo em {IP}:{PORT}')
    
    try:
        while True:
            connection, address = operations_socket.accept()
            print(f'Conectado com {address}\n')

            with connection:
                data = connection.recv(4096).decode().lower()
                if not data:
                    continue
                
                # Envia os parâmetros da requisição para serem pesquisados no cache
                cached = cache.search_operation(data)
                if cached:
                    print('\nOperação já disponível em cache')
                    response = cached
                else:  
                    response = manage_request(data.strip().split('\n'))
                    cache.write_cache(data, str(response))

                connection.sendall(str(response).encode())

    except (socket.error, ConnectionRefusedError) as e:
        raise excepts.RpcServerNotFound(f'\nErro no servidor de operações:\n\n{e}')
    except KeyboardInterrupt:
        print('\n\nServidor de operações encerrado pelo usuário (CTRL+C)')
    finally:
        print('Servidor Finalizando...\n')
        