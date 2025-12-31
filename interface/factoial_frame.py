import tkinter as tk

class FactorialFrame(tk.Frame):
    '''
    
    '''
    def __init__(self, master, operation, on_execute):
        super().__init__(master)

        self.operation = operation
        self.on_execute = on_execute

        # Container principal
        container = tk.Frame(self, bg='#cccccc')
        container.pack(expand=True)

        # Título
        title = tk.Label(container, text="Calculadora de Fatorial", font=('Segoe UI', 22, 'bold'), bg='#cccccc', fg='#2b2b3c')
        title.pack(pady=(50, 30))

        # Subtítulo
        subtitle = tk.Label(container, text="Digite um número inteiro positivo", font=('Segoe UI', 15), bg='#cccccc', fg='#666666')
        subtitle.pack(pady=(0, 20))

        # Campo de entrada
        entry_frame = tk.Frame(container, bg='#cccccc')
        entry_frame.pack(pady=10, padx=30)

        tk.Label( entry_frame, text="Número:", font=('Segoe UI', 12), bg='#cccccc', fg='#2b2b3c').pack(anchor='w')

        self.entry = tk.Entry(entry_frame, font=('Segoe UI', 14), width=20, bg='#ffffff', fg='#2b2b3c', bd=1, relief='solid', insertbackground='#111827')
        self.entry.pack(pady=5, ipady=8)

        # Botão calcular
        btn = tk.Button(
            container, text="Calcular Fatorial", font=('Segoe UI', 12, 'bold'), 
            bg='#111827', fg='#ffffff', activebackground='#000011', activeforeground='#ffffff',
            bd=0, cursor='hand2', width=20, pady=12,
            command=self.execute
        )
        btn.pack(pady=(20, 30), padx=30)

        # Efeito hover
        btn.bind('<Enter>', lambda e: btn.config(bg='#0f172e'))
        btn.bind('<Leave>', lambda e: btn.config(bg='#0f172e'))

    def execute(self):
        value = self.entry.get().strip()
        if value:
            self.on_execute(self.operation, value)
