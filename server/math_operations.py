'''
    Módulo responsável por executar operações matemáticas no lado do servidor.

    As funções convertem os argumentos recebidos como strings, executam a operação
    solicitada e retornam o resultado como string (para envio via socket).
'''

import sys
import math
import multiprocessing


# Permite trabalhar com números de até ~1 milhão de dígitos
sys.set_int_max_str_digits(1_000_000)  


def convertNumbers(*numbers: list[str]) -> list:
    '''
        Converte uma sequência de valores string para uma lista de floats.

        Args:  
            *numbers: Sequência de valores numéricos em formato string.
        Returns:    
            list[float] | str: Lista de números convertidos, ou mensagem de err o.
    '''
    try: 
        # Transforma em um vetor de inteiros
        return [float(n) for n in numbers] 
    except ValueError:
        return '\nErro ao converter números.\n'
    
    
def convertNumber(x: str) -> float:
    '''
        Converte uma string em número float.

        Args: 
            x (str): Valor a ser convertido.
        Returns: 
            float | str: Número convertido ou mensagem de erro.
    '''
    try: 
        return float(x) 
    except ValueError:
        return '\nErro ao converter número.\n'
    

def addition(numbers: list[str]) -> str:
    '''
        Função para somar uma lista de números.
        
        Args: 
            numbers (list[str]): Lista de números em formato string.
        Returns: 
            str: Resultado da soma ou mensagem de erro.'''
    numbers = convertNumbers(*numbers)
    return numbers if isinstance(numbers, str) else sum(numbers)

def subtraction(numbers: list[str]) -> str:
    '''
        Função para subtrair uma lista de números.

        Args: 
            numbers (list[str]): Lista de números em formato string.
        Returns: 
            str: Resultado da subtração ou mensagem de erro.
    '''
    numbers = convertNumbers(*numbers)
    if isinstance(numbers, str):
        return numbers

    result = numbers[0]
    for n in numbers[1:]:
        result -= n
    return result

def multiplication(numbers: list[str]) -> str:
    '''
        Função para multiplicar uma lista de números.

        Args: 
            numbers (list[str]): Lista de números em formato string.
        Returns: 
            str: Resultado da multiplicação ou mensagem de erro.
    '''
    numbers = convertNumbers(*numbers)
    if isinstance(numbers, str):
        return numbers

    result = 1
    for n in numbers:
        result *= n
    return result

def division(numbers: list[str]) -> str:
    '''
        Função para dividir uma lista de números.

        Args: 
            numbers (list[str]): Lista de números em formato string.
        Returns: 
            str: Resultado da divisão ou mensagem de erro.
    '''
    numbers = convertNumbers(*numbers)
    if isinstance(numbers, str):
        return numbers

    result = numbers[0]
    for n in numbers[1:]:
        if n == 0:
            return '\nErro: divisão por zero.\n'
        result /= n
    return result

def factorial(x: str) -> str:
    '''
        Função para calcular o fatorial de um número.

        Args: 
            x (str): Número em formato string.
        Returns: 
            str: Resultado do fatorial ou mensagem de erro.
    '''
    x = convertNumber(x)
    if isinstance(x, str):
        return x

    if x < 0 or not x.is_integer():
        
        return '\nErro: forneça um inteiro não negativo.\n'

    try:
        return str(math.factorial((int)(x)))
    except (OverflowError, MemoryError):
        return '\nErro: cálculo muito grande para ser realizado.\n'

def check_primes(numbers: list[str]) -> str:
    '''
        Função para verificar se os números em uma lista são primos.
        Utiliza multiprocessing para acelerar a verificação.

        Args: 
            numbers (list[str]): Lista de números em formato string.
        Returns: 
            str: Lista de booleanos indicando se cada número é primo, ou mensagem de erro.
    '''
    numbers = convertNumbers(*numbers)  # Desempacota a lista com * para passar os números individualmente
    if isinstance(numbers, str):  # Verifica se houve erro na conversão
        return numbers  # Retorna o erro caso tenha ocorrido

    with multiprocessing.Pool(processes=2) as pool:
        result = pool.map(_is_prime, numbers)

    return result


def _is_prime(number: int) -> bool:
    '''
        Verifica se um número é primo.

        Args:
            number (int): Número a ser verificado.
        Returns: 
            bool: True se for primo, False caso contrário.
    '''
    if number < 2:
        return False
    
    n = number - 1
    
    while n > 1:
        if number % n == 0:
            return False
        n -= 1

    return True 
