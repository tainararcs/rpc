from operations import Operations
from exceptions import RpcServerNotFound  
import server.utils as utils

import datetime


# Configurações de conexão 
IP = utils.get_ip_client()      # Retorna '127.0.0.1'
PORT = utils.get_port_client()  # Retorna 11110


# Teste
try:
    op = Operations(IP, PORT)

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

    numbers_list = list(range(12))
    print('\nPrimos:')
    print('\t -> ', op.check_primes(*numbers_list))

    print('\nNotícias do site da UOL no dia', datetime.date.today(), ':')
    print(op.get_uol_news())

    print()

except RpcServerNotFound as e:
    print(e)