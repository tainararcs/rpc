import tkinter as tk

# usuário digita → clica Calcular → callback → RPC → resultado

class PrimeFrame(tk.Frame):
    def __init__(self, master, operation, on_execute):
        super().__init__(master, bg='#ffffff')

        self.operation = operation
        self.on_execute = on_execute

        # Container principal
        container = tk.Frame(self, bg='#f5f5f5', relief='solid', bd=1)
        container.pack(padx=40, pady=40)

        # Título
        title = tk.Label(
            container,
            text="Verificador de Números Primos",
            font=('Segoe UI', 18, 'bold'),
            bg='#f5f5f5',
            fg='#2b2b3c'
        )
        title.pack(pady=(20, 10))

        # Subtítulo
        subtitle = tk.Label(
            container,
            text="Digite números separados por vírgula (ex: 2, 7, 11, 15)",
            font=('Segoe UI', 10),
            bg='#f5f5f5',
            fg='#666666'
        )
        subtitle.pack(pady=(0, 20))

        # Campo de entrada
        entry_frame = tk.Frame(container, bg='#f5f5f5')
        entry_frame.pack(pady=10, padx=30)

        tk.Label(
            entry_frame,
            text="Números:",
            font=('Segoe UI', 12),
            bg='#f5f5f5',
            fg='#2b2b3c'
        ).pack(anchor='w')

        self.entry = tk.Entry(
            entry_frame,
            font=('Segoe UI', 14),
            width=35,
            bg='#ffffff',
            fg='#2b2b3c',
            bd=1,
            relief='solid',
            insertbackground='#7c3aed'
        )
        self.entry.pack(pady=5, ipady=8)

        # Botão verificar
        btn = tk.Button(
            container,
            text="Verificar Primos",
            font=('Segoe UI', 12, 'bold'),
            bg='#7c3aed',
            fg='#ffffff',
            activebackground='#9333ea',
            activeforeground='#ffffff',
            bd=0,
            cursor='hand2',
            command=self.execute,
            width=20,
            pady=12
        )
        btn.pack(pady=(20, 30), padx=30)

        # Efeito hover
        btn.bind('<Enter>', lambda e: btn.config(bg='#9333ea'))
        btn.bind('<Leave>', lambda e: btn.config(bg='#7c3aed'))

    def execute(self):
        value = self.entry.get().strip()
        if value:
            self.on_execute(self.operation, value)