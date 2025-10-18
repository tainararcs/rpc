# Define a interface de operações para o cliente.

import tcp_client as client
import server.consts as consts

class Operations:
    '''
    Classe responsável por enviar requisições de operações matemáticas para o servidor via socket TCP.
    Constroi a mensagem no formato esperado pelo servidor.

        Formato de mensagem:
            <OPERAÇÃO>\n<ARG1>\n<ARG2>\n...

    Args:
        ip (str): Endereço IP do servidor.
        port (int): Porta TCP do servidor.

    Returns:
        Resultado da operação solicitada em string. 
    '''
    
    def __init__(self, ip: str, port: str):
        self.ip = ip
        self.port = port

    def execute(self, operation: str, *args: str) -> str:
        """
        Monta a operação para ser enviada ao servidor TCP.

        Args:
            operation (str): Tipo de operação (ex: 'sum', 'sub', 'div', etc).
            *args (str): Argumentos numéricos da operação.

        Returns:
            str: Resultado retornado pelo servidor.
        """
        # Monta a mensagem no formato esperado
        message = f"{operation}\n" + "\n".join(str(a) for a in args)
        return client.execute_remote_operation(self.ip, self.port, message)

    def addition(self, *numbers: str) -> str:
        return self.execute(consts.SUM, *numbers)

    def subtraction(self, *numbers: str) -> str:
        return self.execute(consts.SUB, *numbers)

    def multiplication(self, *numbers: str) -> str:
        return self.execute(consts.MUL, *numbers)

    def division(self, *numbers: str) -> str:
        return self.execute(consts.DIV, *numbers)

    def factorial(self, x: str) -> str:
        return self.execute(consts.FAC, x)