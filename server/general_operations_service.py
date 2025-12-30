'''
    Módulo responsável por executar operações matemáticas no lado do servidor.

    As funções convertem os argumentos recebidos como strings, executam a operação
    solicitada e retornam o resultado como string (para envio via socket).
'''

import requests
from bs4 import BeautifulSoup
from google import genai 
import dotenv
import os

dotenv.load_dotenv()

API_KEY = dotenv.get_key(dotenv.find_dotenv(), 'API_KEY')
MODEL = "gemini-2.5-flash"
client = genai.Client(api_key=API_KEY)

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

def math_problem_solver(msg: str) -> str:
    prompt = f'''
        Você é um solucionador de problemas matemáticos.

        1. Resolva o problema a seguir realizando todos os cálculos necessários internamente.
        2. NÃO mostre o passo a passo.
        3. NÃO explique o raciocínio.
        
        4. Retorne uma BREVE explicação do que foi calculado e APENAS o valor final da resposta.
        5. Se houver mais de um resultado válido, retorne todos, separados por vírgula.
        6. Não utilize markdown, listas ou texto adicional.

        Problema: {msg}

        Exemplo de Resposta:
            "Raiz quadrada de 9 = 3
             Raiz quadrada de 121: 11"
        '''.strip()
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text or "Nenhuma resposta gerada."
