import interface.interface as interface
from operations import Operations
from exceptions import RpcServerNotFound  
import server.utils as utils
from tkinter import messagebox

# Configurações de conexão 
IP = utils.get_ip_client()      # Retorna '127.0.0.1'
PORT = utils.get_port_client()  # Retorna 11110

def manage_send_operation(operation: str, payload, op: Operations):
    try:
        match operation:
            case 'sum':
                result = op.addition(*payload)
            case 'sub':
                result = op.subtraction(*payload)
            case 'mul':
                result = op.multiplication(*payload)
            case 'div':
                result = op.division(*payload)
            case 'fac':
                result = op.factorial(payload[0])
            case 'prime':
                result = op.check_primes(*payload)
            case 'news':
                return op.get_uol_news()
            case 'solver':
                result = op.math_problem_solver(payload[0])
            case _:
                raise ValueError("Operação inválida")

        messagebox.showinfo('Resultado', f'{result}')
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