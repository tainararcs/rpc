'''
    Módulo responsável por executar operações matemáticas no lado do servidor.

    As funções convertem os argumentos recebidos como strings, executam a operação
    solicitada e retornam o resultado como string (para envio via socket).
'''

import requests
from bs4 import BeautifulSoup
from google import genai 
import dotenv

dotenv.load_dotenv()

API_KEY = dotenv.get_key(dotenv.find_dotenv(), 'API_KEY')
MODEL = "gemini-2.5-flash"
client = genai.Client(api_key=API_KEY)

def get_uol_news() -> str:
    '''
        Obtém as principais notícias do site da UOL.

        Returns: 
            str: Lista formatada com os títulos das notícias ou mensagem de erro.
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
    formatted = '\n'.join(f'\t• {t}' for t in titles[:15])

    # Retorna apenas os 10 primeiros títulos limpos
    return formatted

def math_problem_solver(msg: str) -> str:
    '''
        Resolve problemas matemáticos descritos em linguagem natural utilizando um modelo de IA generativa.
        Resolve utilizando raciocínio em duas etapas.
        
        1) Primeira chamada → gera um raciocínio detalhado (Chain of Thought).
        2) Segunda chamada → sintetiza apenas uma explicação breve + resposta final, sem revelar cálculos ou passos intermediários.

        Args:
            msg (str): Enunciado do problema matemático.
        Returns:
            str: Resposta textual gerada pelo modelo ou mensagem padrão caso nenhuma resposta seja produzida.
    '''
    cot_prompt = f'''
        Você é um solucionador de problemas matemáticos.

        - Resolva o problema a seguir realizando todos os cálculos necessários.
        - Realize todos os cálculos explicando passo a passo, use o Chain-of-Thought.
        - Mostre todos os passos e cálculos.

        Problema: {msg}
    '''.strip()
    
    cot_response = client.models.generate_content(model=MODEL, contents=cot_prompt)
    cot_response = cot_response.text or "Nenhuma resposta gerada."

    if len(cot_response) > 4000:
            cot_response = cot_response[:4000] + "\n[resumo truncado]\n"

    final_prompt = f'''
        Com base na análise detalhada abaixo: 
        {cot_response}

        - Produza apenas uma breve explicação do que foi calculado e o resultado final.
        - Não mostre cálculos. Não mostre passos.
        - Não explique o raciocínio.
        - Não use markdown, listas ou formatação especial.
        - Se houver mais de uma resposta, retorne todas separadas por vírgula.
        - Retorne uma BREVE explicação do que foi calculado e APENAS o valor final da resposta.
        
        Análise detalhada:\n{cot_response}

        Exemplo de Resposta:
            "Raiz quadrada de 9 = 3
             Raiz quadrada de 121: 11"
    '''.strip()

    final_response = client.models.generate_content(model=MODEL, contents=final_prompt)

    return final_response.text or "Nenhuma resposta gerada."
