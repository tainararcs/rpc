'''
    Módulo responsável por executar operações matemáticas no lado do servidor.

    As funções convertem os argumentos recebidos como strings, executam a operação
    solicitada e retornam o resultado como string (para envio via socket).
'''

import requests
from bs4 import BeautifulSoup


def get_uol_news() -> str:
    '''
        Obtém as principais notícias do site da UOL.

        Returns: 
            str: Lista formatada com os títulos das notícias.
    '''
    url = 'https://www.uol.com.br/'
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return 'Não foi possível obter notícias.'

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Busca todos os títulos principais 
    titles = [t.get_text(strip=True) for t in soup.find_all('h3')]
    
    # Remove duplicados e vazios
    titles = [t for t in titles if t] 

    # Monta string formatada com espaçamento e quebra de linha
    formatted = '\n'.join(f'\t• {t}' for t in titles[:10])

    # Retorna apenas os 10 primeiros títulos limpos
    return formatted