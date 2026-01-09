'''
'    Frame da interface gráfica responsável pela verificação de números primos.Frame da interface gráfica responsável pela verificação de números primos.

'''
import tkinter as tk

class PrimeFrame(tk.Frame):
    def __init__(self, master: tk.Widget, operation: str, on_execute) -> None:
        '''
            Inicializa o frame de verificação de números primos.

            Args:
                master (tk.Widget): Widget pai.
                operation (str): Identificador da operação RPC (ex.: 'prime').
                on_execute (Callable): Callback para execução RPC.
        '''
        super().__init__(master, bg='#cccccc')

        self.operation = operation
        self.on_execute = on_execute
    
        # Container principal
        container = tk.Frame(self, bg='#cccccc', bd=1)
        container.pack(padx=40, pady=40)

        # Título
        title = tk.Label(
            container, text="Verificador de Números Primos",
            font=('Segoe UI', 22, 'bold'), bg='#cccccc',fg='#2b2b3c'
        )
        title.pack(pady=(20, 10))

        # Subtítulo
        subtitle = tk.Label(
            container, text="Digite números separados por vírgula (ex: 2, 7, 11, 15)",
            font=('Segoe UI', 15), bg='#cccccc', fg="#050000"
        )
        subtitle.pack(pady=(0, 20))

        # Campo de entrada
        entry_frame = tk.Frame(container, bg='#cccccc')
        entry_frame.pack(pady=10, padx=30)

        tk.Label(
            entry_frame, text="Números:",
            font=('Segoe UI', 12), bg='#cccccc', fg='#2b2b3c'
        ).pack(anchor='w')

        self.entry = tk.Entry(
            entry_frame,
            font=('Segoe UI', 14), width=35,
            bg='#f5f5f5', fg='#2b2b3c',
            bd=1, insertbackground='#111827'
        )
        self.entry.pack(pady=5, ipady=8)

        # Botão verificar
        btn = tk.Button(
            container, text="Verificar Primos",
            font=('Segoe UI', 12, 'bold'),
            bg='#111827', fg='#ffffff',
            activebackground='#0f172e', activeforeground='#ffffff',
            bd=0, cursor='hand2',
            command=self.execute,
            width=20, pady=12
        )
        btn.pack(pady=(20, 30), padx=30)

        self.output = tk.Label(self,  text="", font=('Segoe UI', 14), bg='#cccccc')
        self.output.pack(pady=20)
        
        # Efeito hover
        btn.bind('<Enter>', lambda e: btn.config(bg='#0f172e'))
        btn.bind('<Leave>', lambda e: btn.config(bg='#0f172e'))

    def execute(self) -> None:
        '''
            Executa a verificação de números primos via callback RPC e exibe o resultado.
        '''
        value = self.entry.get().strip()
        result = self.on_execute(self.operation, value)
        self.show_result(result)

    def show_result(self, result: str) -> None:
        '''
            Exibe o resultado da verificação no label de saída.

            Args:
                result (Any): Resultado retornado pela operação RPC.
        '''
        if result is None:
            self.output.config(text="Resultado inválido.")
            return

        self.output.config(text=f"Resultado:\n{result}")