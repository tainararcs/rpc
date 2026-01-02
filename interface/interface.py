import server.consts as consts
from operations import Operations
from interface.prime_frame import PrimeFrame
from interface.calculator_frame import CalculatorFrame
from interface.factorial_frame import FactorialFrame
from interface.chat_frame import ChatFrame
from interface.news_frame import NewsFrame
from interface.home_frame import HomeFrame
import tkinter as tk

CALC_HOME = {consts.HOME}
CALC_OPS = {consts.CALC, consts.SUM, consts.SUB, consts.MUL, consts.DIV}
FAC_OPS = {consts.FAC}
PRIME_OPS = {consts.PRIME}
CHAT_OPS = {consts.SOLVER}
NO_INPUT_OPS = {consts.NEWS}

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

def create_interface():
    '''
    '''
    window = tk.Tk()
    window.title('RPC')
    window.geometry('1200x800')
    window.configure(bg=COLORS['bg_main'])
    window.minsize(900, 600)
    return window

def manage_interface_rpc(window, on_execute):
    '''
    '''
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, minsize=280)
    window.grid_columnconfigure(1, weight=1)
    
    # Menu lateral esquerdo
    menu_container = tk.Frame(window, bg=COLORS['bg_menu'])
    menu_container.grid(row=0, column=0, sticky='nsew')
    menu_container.grid_propagate(True)
    menu_container.config(width=280)
    
    # Área de conteúdo da direita
    content_container = tk.Frame(window, bg=COLORS['bg_content'])
    content_container.grid(row=0, column=1, sticky='nsew')
    
    header_frame = tk.Frame(content_container, bg='#cccccc', height=80)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    header_content = tk.Frame(header_frame, bg='#cccccc')
    header_content.place(relx=0.5, rely=0.5, anchor='center')
    
    logo_label = tk.Label(
        menu_container, text='RPC',
        font=('Segoe UI', 24, 'bold'), height=2,
        bg=COLORS['bg_main'], fg=COLORS['text_light']
    )
    logo_label.pack()
    
    subtitle_label = tk.Label(
        menu_container, text='Remote Procedure Call',
        font=('Segoe UI', 8), height=2,
        bg=COLORS['bg_main'], fg=COLORS['border']
    )
    subtitle_label.pack()

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
    selected_button = {'btn': None}
    
    def show_home():
        '''
        '''
        if current_frame['frame']:
            current_frame['frame'].destroy()
        
        header_label.config(text='Bem-vindo ao RPC')
        
        home = HomeFrame(main_content)
        home.pack(fill='both', expand=True)
        current_frame['frame'] = home
        
        # Reseta seleção de botão
        if selected_button['btn']:
            selected_button['btn'].config(bg=COLORS['bg_menu'])
            selected_button['btn'] = None
    
    def on_operation_selected(operation, btn):
        '''
        '''
        if operation in CALC_HOME:
            show_home()
            return
    
        title = MENU_ITEMS.get(operation, "Operação")
        header_label.config(text=title)
        
        if selected_button['btn']:
            selected_button['btn'].config(bg=COLORS['bg_menu'])
        btn.config(bg=COLORS['accent'])
        selected_button['btn'] = btn
        
        if current_frame['frame']:
            current_frame['frame'].destroy()
        
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

    for operation, text in MENU_ITEMS.items():
        btn_container = tk.Frame(menu_container, bg=COLORS['bg_menu'])
        btn_container.pack(fill='x', padx=12, pady=4)
        
        btn = tk.Button(
            btn_container, text=text,
            font=('Segoe UI', 11),
            bg=COLORS['bg_menu'], fg=COLORS['text_light'],
            activebackground=COLORS['accent_hover'],
            activeforeground=COLORS['text_light'],
            bd=0, relief='flat',
            highlightthickness=0,
            pady=14, cursor='hand2',
            anchor='w', padx=20,
            command=lambda op=operation, b=None: (setattr(b, 'self', btn) if b is None else None, on_operation_selected(op, btn))
        )
        btn.pack(fill='x')
        
        # Configura o command 
        btn.config(command=lambda op=operation, b=btn: on_operation_selected(op, b))
        
        # Efeito hover 
        def on_enter(e, button=btn):
            if button != selected_button['btn']:
                button.config(bg=COLORS['accent_hover'])
        
        def on_leave(e, button=btn):
            if button != selected_button['btn']:
                button.config(bg=COLORS['bg_menu'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
    
    # Rodapé do menu
    footer = tk.Label(
        menu_container,
        text='© 2026 RPC System',
        font=('Segoe UI', 8), justify='center',
        bg=COLORS['bg_menu'], fg=COLORS['border'],   
    )
    footer.pack(side='bottom', pady=15)
    
    show_home()
