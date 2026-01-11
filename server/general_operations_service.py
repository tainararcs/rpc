'''
    Módulo responsável por executar operações matemáticas no lado do servidor.

    As funções convertem os argumentos recebidos como strings, executam a operação
    solicitada e retornam o resultado como string (para envio via socket).
'''

import requests
import json
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
    try:
        prompt = f'''
            Você é um solucionador de problemas matemáticos.

            Resolva o problema abaixo seguindo as etapas:
            1. Pense passo a passo e explique todo o raciocínio detalhadamente.
            2. Em seguida produza apenas uma breve explicação + resposta final sem mostrar cálculos.

            IMPORTANTE:
            - A saída DEVE ser estritamente um JSON válido.
            - Não escreva nada fora do JSON.
            - O JSON deve ter exatamente esta estrutura:
            - Não use markdown, listas ou formatação especial.

            {{
                "cot": "seu raciocínio passo a passo aqui",
                "final_answer": "breve explicação + resposta final aqui"
            }}

            Exemplo de Resposta para final_answer:
                "Raiz quadrada de 9 = 3"
                "Raiz quadrada de 121: 11"

            Problema: {msg}
        '''.strip()
        
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        text = response.text or ""
        if not text:
            return "Nenhuma resposta gerada."

        # Tenta interpretar JSON
        data = json.loads(text)

        final = data.get("final_answer", "").strip()
        return final if final else "Nenhuma resposta gerada."

    except json.JSONDecodeError:
        return "Erro: o modelo não retornou um JSON válido."
    except Exception as e:
        return f"Erro ao resolver problema: {e}"