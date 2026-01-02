'''
    Frame da interface gráfica responsável pelo cálculo de fatorial.
    Permite ao usuário informar um número inteiro positivo e encaminha a operação para o servidor RPC.
'''

import tkinter as tk

class FactorialFrame(tk.Frame):
    '''
        Frame para cálculo de fatorial via RPC.
    '''
    def __init__(self, master: tk.Widget, operation: str, on_execute) -> None:
        '''
            Inicializa o frame de fatorial.

            Args:
                master (tk.Widget): Widget pai.
                operation (str): Identificador da operação RPC (ex.: 'fac').
                on_execute (Callable): Callback para execução RPC.
        '''
        super().__init__(master, bg='#cccccc')

        self.operation = operation
        self.on_execute = on_execute

        # Container principal
        container = tk.Frame(self, bg='#cccccc')
        container.pack(expand=True)

        # Título
        title = tk.Label(
            container, text="Calculadora de Fatorial", 
            font=('Segoe UI', 22, 'bold'), bg='#cccccc', fg='#2b2b3c'
        )
        title.pack(pady=(50, 30))

        # Subtítulo
        subtitle = tk.Label(
            container, text="Digite um número inteiro positivo", 
            font=('Segoe UI', 15), bg='#cccccc', fg='#666666'
        )
        subtitle.pack(pady=(0, 20))

        # Campo de entrada
        entry_frame = tk.Frame(container, bg='#cccccc')
        entry_frame.pack(pady=10, padx=30)

        tk.Label( entry_frame, text="Número:", font=('Segoe UI', 12), bg='#cccccc', fg='#2b2b3c').pack(anchor='w')

        self.entry = tk.Entry(
            entry_frame, font=('Segoe UI', 14),
            width=20, bg='#ffffff', fg='#2b2b3c',
            bd=1, insertbackground='#111827'
        )
        self.entry.pack(pady=5, ipady=8)

        # Botão calcular
        btn = tk.Button(
            container, text="Calcular Fatorial", font=('Segoe UI', 12, 'bold'), 
            bg='#111827', fg='#ffffff', activebackground='#000011', activeforeground='#ffffff',
            bd=0, cursor='hand2', width=20, pady=12,
            command=self.execute
        )
        btn.pack(pady=(20, 30), padx=30)

        self.output = tk.Label(self,  text="", font=('Segoe UI', 14), bg='#cccccc')
        self.output.pack(pady=20)

        # Efeito hover
        btn.bind('<Enter>', lambda e: btn.config(bg='#0f172e'))
        btn.bind('<Leave>', lambda e: btn.config(bg='#0f172e'))

    def execute(self) -> None:
        '''
            Executa a operação de fatorial via callback RPC e exibe o resultado.
        '''
        value = self.entry.get().strip()
        result = self.on_execute(self.operation, value)
        self.show_result(result)

    def show_result(self, result: str) -> None:
        '''
            Exibe o resultado da operação no label de saída.

            Args:
                result (Any): Resultado retornado pela operação RPC.
        '''
        if result is None:
            self.output.config(text="Resultado inválido.")
            return

        self.output.config(text=f"Resultado: {result}")
