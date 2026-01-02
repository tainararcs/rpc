'''
    Módulo responsável pelo menu lateral da interface gráfica.
    Define o MenuFrame, que permite selecionar as operações disponíveis na aplicação RPC.
'''
import server.consts as consts
import tkinter as tk

class MenuFrame(tk.Frame):
    '''
        Frame que representa o menu lateral da aplicação.
    '''
    def __init__(self, master: tk.Widget, on_select) -> None:
        '''
            Inicializa o menu lateral.

            Args:
                master (tk.Widget): Widget pai.
                on_select (Callable): Callback chamado ao selecionar uma operação.
        '''
        super().__init__(master, bg='#111827')
        self.on_select = on_select
        self.selected_btn = None

        self.buttons = {
            consts.HOME: "⌂ Home",
            consts.CALC: "∑ Calculadora",
            consts.FAC: "! Fatorial",
            consts.PRIME: "✓ Número Primo",
            consts.NEWS: "▤ Notícias UOL",
            consts.SOLVER: "›› Resolvedor com IA",
        } 

        logo_label = tk.Label(
            self, text='RPC',
            font=('Segoe UI', 24, 'bold'), height=2,
            bg='#111827', fg='white'
        )
        logo_label.pack()
        
        subtitle_label = tk.Label(
            self, text='Remote Procedure Call',
            font=('Segoe UI', 8), height=2,
            bg='#111827', fg='#334155'
        )
        subtitle_label.pack()

        # Botões do menu
        for op, text in self.buttons.items():
            btn = tk.Button(
                self, text=text, font=('Segoe UI', 11),
                bg='#111827', fg='#ffffff', bd=0,
                anchor='w', padx=20, pady=14, cursor='hand2', highlightthickness=0, 
                activebackground='#000011', activeforeground='#ffffff',
                command=lambda o=op, b=None: self.select(o, b)
            )
            btn.pack(fill='x', padx=12, pady=4)

            btn.config(command=lambda o=op, b=btn: self.select(o, b))
        
        # Rodapé do menu
        footer = tk.Label(
            self,
            text='© 2026 RPC System',
            font=('Segoe UI', 8), justify='center',
            bg='#111827', fg='#334155'
        )
        footer.pack(side='bottom', pady=15)

    def select(self, operation: str, button: tk.Button) -> None:
        '''
            Seleciona uma operação no menu, atualizando o destaque visual e chamando o callback de seleção.

            Args:
                operation (str): Identificador da operação selecionada.
                button (tk.Button): Botão correspondente à operação.
        '''
        if self.selected_btn:
            self.selected_btn.config(bg='#111827')

        button.config(bg='#2563eb')
        self.selected_btn = button
        self.on_select(operation)
