"""
Módulo responsável por executar operações matemáticas no lado do servidor.

As funções convertem os argumentos recebidos como strings, executam a operação
solicitada e retornam o resultado como string (para envio via socket).
"""
import sys
import math
import requests
from bs4 import BeautifulSoup

# Permite trabalhar com números de até ~1 milhão de dígitos
sys.set_int_max_str_digits(1_000_000)  

def convertNumbers(*numbers: list[str]) -> list[float]:
    """
    Converte uma sequência de valores string para uma lista de floats.

    Args: *numbers: Sequência de valores numéricos em formato string.
    Returns: list[float] | str: Lista de números convertidos, ou mensagem de erro.
    """
    try: 
        # Transforma em um vetor de inteiros
        return [float(n) for n in numbers] 
    except ValueError:
        return "\nErro ao converter números inteiros.\n"
    
def convertNumber(x: str) -> float:
    """
    Converte uma string em número float.

    Args: x (str): Valor a ser convertido.
    Returns: float | str: Número convertido ou mensagem de erro.
    """
    try: 
        return float(x) 
    except ValueError:
        return "\nErro ao converter número inteiro.\n"
    

def addition(numbers: list[str]) -> str:
    numbers = convertNumbers(*numbers)
    return numbers if isinstance(numbers, str) else sum(numbers)

def subtraction(numbers: list[str]) -> str:
    numbers = convertNumbers(*numbers)
    if isinstance(numbers, str):
        return numbers

    result = numbers[0]
    for n in numbers[1:]:
        result -= n
    return result

def multiplication(numbers: list[str]) -> str:
    numbers = convertNumbers(*numbers)
    if isinstance(numbers, str):
        return numbers

    result = 1
    for n in numbers:
        result *= n
    return result

def division(numbers: list[str]) -> str:
    numbers = convertNumbers(*numbers)
    if isinstance(numbers, str):
        return numbers

    result = numbers[0]
    for n in numbers[1:]:
        if n == 0:
            return "\nErro: divisão por zero.\n"
        result /= n
    return result

def factorial(x: str) -> str:
    x = convertNumber(x)
    if isinstance(x, str):
        return x

    if x < 0 or not x.is_integer():
        return "\nErro: forneça um inteiro não negativo.\n"

    try:
        return str(math.factorial((int)(x)))
    except (OverflowError, MemoryError):
        return "\nErro: cálculo muito grande para ser realizado.\n"

def get_uol_news() -> str:
    url = "https://www.uol.com.br/"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return "Não foi possível obter notícias."

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Busca todos os títulos principais 
    titles = [t.get_text(strip=True) for t in soup.find_all('h3')]
    
    # Remove duplicados e vazios
    titles = [t for t in titles if t] 

    # Monta string formatada com espaçamento e quebra de linha
    formatted = "\n".join(f"\t• {t}" for t in titles[:10])

    # Retorna apenas os 10 primeiros títulos limpos
    return formatted