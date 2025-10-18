class RpcServerNotFound(Exception):
    '''
    Exceção personalizada lançada quando não é possível estabelecer conexão com o servidor RPC remoto.
    '''
    def __init__(self, message = "Erro ao tentar conexão com servidor"):
        super().__init__(message)
