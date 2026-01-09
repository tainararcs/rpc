'''
    Módulo principal da aplicação cliente RPC.
    Iinicializa a interface gráfica, configura a conexão com o servidor RPC 
    e faz o roteamento entre eventos da interface e chamadas de operações remotas.
'''
import interface.interface as interface
from client.operations import Operations
from server.exceptions import RpcServerNotFound  
import server.utils as utils
from tkinter import messagebox

# Configurações de conexão 
IP = utils.get_ip_client_server()      # Retorna '127.0.0.1'
PORT = utils.get_port_client_server()  # Retorna 11110

def manage_send_operation(operation: str, payload, op: Operations) -> str:
    '''
    Encaminha uma operação solicitada pela interface gráfica para o cliente RPC apropriado.
    Atua como um dispatcher entre a UI e o objeto Operations, traduzindo o identificador da operação para a chamada RPC correspondente.

    Args:
        operation (str): Identificador da operação (ex.: 'sum', 'news').
        payload (Iterable[Any]): Argumentos associados à operação.
        op (Operations): Instância do cliente RPC.
    Returns:
        str | None: Resultado retornado pelo servidor RPC, ou None em caso de erro tratado.
    '''
    try:
        match operation:
            case 'sum':
                return op.addition(*payload)
            case 'sub':
                return op.subtraction(*payload)
            case 'mul':
                return op.multiplication(*payload)
            case 'div':
                return op.division(*payload)
            case 'fac':
                return op.factorial(payload[0])
            case 'prime':
                return op.check_primes(*payload)
            case 'news':
                return op.get_uol_news()
            case 'solver':
                return op.math_problem_solver(payload[0])
            case _:
                raise ValueError("Operação inválida")
    
    except Exception as e:
        messagebox.showerror('Erro', str(e))

def main():
    '''
        Função principal da aplicação.

        Responsabilidades:
        - Instanciar o cliente RPC.
        - Criar a interface gráfica.
        - Conectar eventos da interface às operações RPC.
        - Iniciar o loop principal da UI.
    '''
    try:
        op = Operations(IP, PORT)

        window = interface.create_interface()
        # Registra o callback que liga a UI às chamadas RPC
        interface.manage_interface_rpc(window, lambda operation, *payload: manage_send_operation(operation, payload, op))
        window.mainloop() 

    except RpcServerNotFound as e:
        print(e)

if __name__ == '__main__':
    main()