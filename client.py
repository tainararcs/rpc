from Operations import Operations
from exceptions import RpcServerNotFound  

import datetime
import json

# Lê o arquivo de configurações
with open('server/configuracoes.txt', 'r') as f:
    config = json.load(f)

# Configurações de conexão 
HOST = config.get('ip')  # Retorna '127.0.0.1'
PORT = config.get('port')  # Retorna 11100

# Teste

try:
    op = Operations(HOST, PORT)

    print('\nSoma:')
    print('\t115.5 + 10 -> ', op.addition(2, 1))
    print('\t115.5 + 10 -> ', op.addition(3, 1))
    print('\t115 + 10 + 30 -> ', op.addition(115, 10, 30))

    print('\nSubtração:')
    print('\t10 - 115 -> ', op.subtraction(115.0, 10.1))
    print('\t115 - 5 - 10 -> ', op.subtraction(115, 5, 10))
    r = op.subtraction(op.subtraction(10.0, 0), op.subtraction(5.0, 0))
    print('\t10 - 0 -> ', r)

    print('\nMultiplicação:')
    print('\t5 * 10 -> ', op.multiplication(5.0, 10.0))
    print('\t5 * 50 * 2 -> ', op.multiplication(5, 50, 2))

    print('\nDivisão:')
    print('\t3 / 10 -> ', op.division(3, 10))
    print('\t50 / 3 / 10 -> ', op.division(50, 3, 10))

    print('\nFatorial:')
    print('\t8 -> ', op.factorial(8.0))
    print('\t10 -> ', op.factorial(10.0))
    print('\t8-> ', op.factorial(8.0))
    print('\t102-> ', op.factorial(102))

    print('\Primos:')
    print('\t -> ', op.factorial(8.0))
    print('\t -> ', op.factorial(10.0))
    print('\t -> ', op.factorial(8.0))
    print('\t -> ', op.factorial(102))


    print('\nNotícias do site da UOL no dia', datetime.date.today(), ':')
    print(op.get_uol_news())

except RpcServerNotFound as e:
    print(e)
