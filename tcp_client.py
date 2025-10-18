# Socket cliente

import socket
import exceptions
import server.consts as consts

# Dicionário simples para simular cache em memória principal
cache: dict[str, str] = {}

def search_operation(operation: str) -> str | None:
    """
    Verifica se o resultado de uma operação já está armazenado em cache.

    Args:
        operation (str): Representação textual da operação (ex: 'sum\\n2\\n3').

    Returns:
        str | None: O resultado armazenado, ou None se a operação não estiver em cache.
    """
    return cache.get(operation.strip())

def write_cache(operation: str, result: str) -> None:
    """
    Armazena o resultado de uma operação no cache em memória.

    Args:
        operation (str): Representação textual da operação.
        result (str): Resultado da operação.
    """
    cache[operation.strip()] = result.strip()

def create_connection(host: str, port: str):
    """
    Cria e retorna um socket TCP conectado ao servidor especificado.

    Args:
        host (str): Endereço IP do servidor.
        port (int): Porta TCP do servidor.

    Returns:
        socket.socket: Objeto socket já conectado.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def execute_remote_operation(host: str, port: int, operation: str) -> str:
    """
    Executa uma operação remota via RPC utilizando um servidor TCP.
    Caso a operação não esteja em cache, ela é enviada ao servidor e o resultado é armazenado no cache local.

    Args:
        host (str): Endereço IP do servidor.
        port (int): Porta TCP do servidor.
        operation (str): Operação a ser executada (ex: 'sum\\n2\\n3').

    Returns:
        str: Resultado retornado pelo servidor ou obtido do cache.

    Raises:
        exceptions.RpcServerNotFound: Se a conexão não puder ser estabelecida.
        socket.error: Em caso de erro na transmissão de dados.
    """
    cached_result = search_operation(operation)
    if cached_result:
        print("\nPegou do cache:")
        return cached_result

    try:
        with create_connection(host, port) as client_socket:
            # Envia a operação codificada
            client_socket.sendall(operation.encode())

            # Aguarda e decodifica a resposta
            result = client_socket.recv(4096).decode()

            # Armazena no cache local
            write_cache(operation, result)
            return result

    except (socket.error, ConnectionRefusedError) as e:
        raise exceptions.RpcServerNotFound(f"Erro ao comunicar com o servidor {host}:{port}\n\n{e}")