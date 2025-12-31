import server.consts as consts
from operations import Operations
from interface.prime_frame import PrimeFrame
from interface.menu_frame import MenuFrame
from interface.calculator_frame import CalculatorFrame
from interface.factoial_frame import FactorialFrame
from interface.chat_frame import ChatFrame
from interface.news_frame import NewsFrame
import tkinter as tk

CALC_OPS = {consts.CALC, consts.SUM, consts.SUB, consts.MUL, consts.DIV}
FAC_OPS = {consts.FAC}
PRIME_OPS = {consts.PRIME}
CHAT_OPS = {consts.SOLVER}
NO_INPUT_OPS = {consts.NEWS}

MENU_ITEMS = {
    consts.CALC: "🧮 Calculadora",
    consts.FAC: "📊 Fatorial",
    consts.PRIME: "🔢 Número Primo",
    consts.NEWS: "📰 Notícias UOL",
    consts.SOLVER: "🤖 Resolvedor com IA",
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


def create_interface():
    window = tk.Tk()
    window.title('Remote Procedure Call')
    window.geometry('1200x800')
    window.configure(bg=COLORS['bg_main'])
    window.minsize(900, 600)
    return window

def manage_interface_rpc(window, on_execute):
    
    # Container principal usando grid
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, minsize=260)
    window.grid_columnconfigure(1, weight=1)
    
    # MENU LATERAL ESQUERDO
    menu_container = tk.Frame(window, bg=COLORS['bg_menu'])
    menu_container.grid(row=0, column=0, sticky='nsew')
    menu_container.grid_propagate(False)
    
    # Título do menu
    title_label = tk.Label(menu_container, text='RPC Menu', font=('Segoe UI', 18, 'bold'), bg=COLORS['bg_menu'], fg=COLORS['text_light'], pady=20)
    title_label.pack(fill='x')
    
    # ÁREA DE CONTEÚDO DIREITA
    content_container = tk.Frame(window, bg=COLORS['bg_content'])
    content_container.grid(row=0, column=1, sticky='nsew', padx=2, pady=2)
    
    # Header da área de conteúdo
    header_frame = tk.Frame(content_container, bg=COLORS['bg_content'], height=60)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    header_label = tk.Label(header_frame, text='Bem-vindo ao RPC', font=('Segoe UI', 25, 'bold'), bg=COLORS['bg_content'], fg=COLORS['bg_main'])
    header_label.pack(expand=True)
    
    # Container para os frames de conteúdo 
    main_content = tk.Frame(content_container, bg=COLORS['bg_content'])
    main_content.pack(fill='both', expand=True, padx=20, pady=20)
    
    current_frame = {'frame': None}
    
    def on_operation_selected(operation):
        title = MENU_ITEMS.get(operation, "Operação")
        header_label.config(text=title)
        
        # Remove frame anterior
        if current_frame['frame']:
            current_frame['frame'].destroy()
        
        # Cria novo frame centralizado
        frame_wrapper = tk.Frame(main_content, bg=COLORS['bg_content'])
        frame_wrapper.place(relx=0.5, rely=0.5, anchor='center')
        
        if operation in CALC_OPS:
            new_frame = CalculatorFrame(frame_wrapper, on_execute)
        elif operation in FAC_OPS:
            new_frame = FactorialFrame(frame_wrapper, operation, on_execute)
        elif operation in PRIME_OPS:
            new_frame = PrimeFrame(frame_wrapper, operation, on_execute)
        elif operation in CHAT_OPS:
            new_frame = ChatFrame(frame_wrapper, operation, on_execute)
        elif operation in NO_INPUT_OPS:
            new_frame = NewsFrame(frame_wrapper)
            result = on_execute(operation, None)
            new_frame.set_text(result)
        
        new_frame.pack()
        current_frame['frame'] = frame_wrapper

    # Botões do menu
    for operation, text in MENU_ITEMS.items():
        btn = tk.Button(
            menu_container, text=text, font=('Segoe UI Emoji', 11),
            bg=COLORS['bg_menu'], fg=COLORS['text_light'], activebackground=COLORS['accent_hover'], activeforeground=COLORS['text_light'],
            bd=0, relief='flat', highlightthickness=0, pady=15, cursor='hand2', anchor='w', padx=20,
            command=lambda op=operation: on_operation_selected(op)
        )
        btn.pack(fill='x', padx=10, pady=5)
        
        # Efeito hover
        def on_enter(e, button=btn):
            button.config(bg=COLORS['accent_hover'])
        
        def on_leave(e, button=btn):
            button.config(bg=COLORS['bg_menu'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
    
    # Rodapé do menu
    footer = tk.Label(menu_container, text='Remote Procedure Call', font=('Segoe UI', 9), bg=COLORS['bg_menu'], fg=COLORS['border'])
    footer.pack(side='bottom', pady=20)