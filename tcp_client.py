# Socket cliente

import socket
import exceptions
import server.consts as consts

def create_connection(host: str, port: str):
    """
    Cria e retorna um socket TCP conectado ao servidor especificado.

    Args:
        host (str): Endereço IP do servidor.
        port (int): Porta TCP do servidor.
    Returns: socket.socket: Objeto socket já conectado.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def execute_remote_operation(host: str, port: int, operation: str) -> str:
    """
    Executa uma operação remota via RPC utilizando um servidor TCP.

    Args:
        host (str): Endereço IP do servidor.
        port (int): Porta TCP do servidor.
        operation (str): Operação a ser executada (ex: 'sum\\n2\\n3').
    Returns: str: Resultado retornado pelo servidor.
    Raises:
        exceptions.RpcServerNotFound: Se a conexão não puder ser estabelecida.
        socket.error: Em caso de erro na transmissão de dados.
    """
    try:
        with create_connection(host, port) as client_socket:
            # Envia a operação codificada
            client_socket.sendall(operation.encode())

            # Aguarda e retorna a resposta decodifica 
            return client_socket.recv(4096).decode()

    except (socket.error, ConnectionRefusedError) as e:
        raise exceptions.RpcServerNotFound(f"Erro ao comunicar com o servidor {host}:{port}\n\n{e}")