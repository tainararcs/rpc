'''
    Definição de exceções personalizadas do sistema RPC.
'''

class RpcServerNotFound(Exception):
    '''
        Exceção personalizada lançada quando não é possível estabelecer conexão com o servidor RPC remoto.
    '''
    def __init__(self, message = 'Erro ao tentar conexão com servidor'):
        super().__init__(message)

class OperationNotFound(Exception):
    '''
        Exceção lançada quando uma operação solicitada não é encontrada ou não está registrada no sistema.
    '''
    def __init__(self, message = 'Erro ao buscar operação'):
        super().__init__(message)