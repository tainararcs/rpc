'''
    Módulo de interface gráfica principal da aplicação RPC.

    Responsável por:
    - Criar a janela principal.
    - Organizar o layout (menu lateral e área de conteúdo).
    - Gerenciar a troca dinâmica de frames conforme a operação selecionada.
'''
import server.consts as consts
from interface.menu_frame import MenuFrame
from interface.prime_frame import PrimeFrame
from interface.calculator_frame import CalculatorFrame
from interface.factorial_frame import FactorialFrame
from interface.chat_frame import ChatFrame
from interface.news_frame import NewsFrame
from interface.home_frame import HomeFrame
import tkinter as tk

# Conjuntos de operações
CALC_HOME = {consts.HOME}
CALC_OPS = {consts.CALC, consts.SUM, consts.SUB, consts.MUL, consts.DIV}
FAC_OPS = {consts.FAC}
PRIME_OPS = {consts.PRIME}
CHAT_OPS = {consts.SOLVER}
NO_INPUT_OPS = {consts.NEWS}

# Labels do menu
MENU_ITEMS = {
    consts.HOME: "⌂ Home",
    consts.CALC: "∑ Calculadora",
    consts.FAC: "! Fatorial",
    consts.PRIME: "✓ Número Primo",
    consts.NEWS: "▤ Notícias UOL",
    consts.SOLVER: "›› Resolvedor com IA",
}

# Cores do tema
COLORS = {
    'bg_main': '#0f172a',        # Azul bem escuro 
    'bg_menu': '#111827',        # Azul acinzentado
    'bg_content': '#cccccc',     # Cinza claro
    'accent': '#2563eb',         # Azul principal 
    'accent_hover': '#000011',   # Azul hover
    'text_light': '#ffffff',
    'text_dark': '#0f172a',
    'border': '#334155',
}

def create_interface() -> tk.Tk:
    '''
        Cria e configura a janela principal da aplicação.

        Returns:
            tk.Tk: Instância configurada da janela principal.
    '''
    window = tk.Tk()
    window.title('RPC')
    window.geometry('1200x800')
    window.configure(bg=COLORS['bg_main'])
    window.minsize(900, 600)
    return window

def manage_interface_rpc(window: tk.Tk, on_execute) -> None:
    '''
        Gerencia o layout da interface e integra a UI com o callback RPC.

        Args:
            window (tk.Tk): Janela principal da aplicação.
            on_execute (Callable): Função callback que executa a operação RPC.
    '''
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, minsize=280)
    window.grid_columnconfigure(1, weight=1)
    
    # Menu lateral esquerdo
    menu_container = MenuFrame(window, on_select=lambda operation: on_operation_selected(operation))
    menu_container.grid(row=0, column=0, sticky='nsew')
    
    # Área de conteúdo da direita
    content_container = tk.Frame(window, bg=COLORS['bg_content'])
    content_container.grid(row=0, column=1, sticky='nsew')
    
    header_frame = tk.Frame(content_container, bg='#cccccc', height=80)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    header_content = tk.Frame(header_frame, bg='#cccccc')
    header_content.place(relx=0.5, rely=0.5, anchor='center')

    header_label = tk.Label(
        header_content,
        text="Bem-vindo ao RPC",
        font=('Segoe UI', 26, 'bold'),
        bg='#cccccc', fg=COLORS['bg_main']
    )
    header_label.pack()
    
    # Container para os frames de conteúdo
    main_content = tk.Frame(content_container, bg=COLORS['bg_content'])
    main_content.pack(fill='both', expand=True)
    
    current_frame = {'frame': None}
    
    def show_home():
        '''
            Exibe o frame inicial (home) na área de conteúdo.
        '''
        if current_frame['frame']:
            current_frame['frame'].destroy()
        
        header_label.config(text='Bem-vindo ao RPC')
        
        home = HomeFrame(main_content)
        home.pack(fill='both', expand=True)
        current_frame['frame'] = home
    
    def on_operation_selected(operation):
        '''
            Callback chamado quando uma operação é selecionada no menu.
            Manipula a troca de frames conforme a operação selecionada.

            Args:
                operation (str): Identificador da operação selecionada.
        '''
        if operation in CALC_HOME:
            show_home()
            return
    
        # Atualiza o título do header
        title = MENU_ITEMS.get(operation, "Operação")
        header_label.config(text=title)

        # Remove o frame atual
        if current_frame['frame']:
            current_frame['frame'].destroy()
        
        # Wrapper do conteúdo
        frame_wrapper = tk.Frame(main_content, bg=COLORS['bg_content'])
        frame_wrapper.pack(fill='both', expand=True)

        content_center = tk.Frame(frame_wrapper, bg=COLORS['bg_content'])
        content_center.pack(fill='both', expand=True)

        if operation in CALC_OPS:
            new_frame = CalculatorFrame(content_center, on_execute)
        elif operation in FAC_OPS:
            new_frame = FactorialFrame(content_center, operation, on_execute)
        elif operation in PRIME_OPS:
            new_frame = PrimeFrame(content_center, operation, on_execute)
        elif operation in CHAT_OPS:
            new_frame = ChatFrame(content_center, operation, on_execute)
        elif operation in NO_INPUT_OPS:
            new_frame = NewsFrame(content_center)
            result = on_execute(operation, None)
            new_frame.set_text(result)
        
        new_frame.pack()
        current_frame['frame'] = frame_wrapper
    
    show_home()
