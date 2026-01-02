import interface.interface as interface
from client.operations import Operations
from server.exceptions import RpcServerNotFound  
import server.utils as utils
from tkinter import messagebox

# Configurações de conexão 
IP = utils.get_ip_client()      # Retorna '127.0.0.1'
PORT = utils.get_port_client()  # Retorna 11110

def manage_send_operation(operation: str, payload, op: Operations):
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
    try:
        op = Operations(IP, PORT)

        window = interface.create_interface()
        interface.manage_interface_rpc(window, lambda operation, *payload: manage_send_operation(operation, payload, op))
        window.mainloop() # Loop principal da interface gráfica que a mantém aberta

    except RpcServerNotFound as e:
        print(e)

if __name__ == '__main__':
    main()