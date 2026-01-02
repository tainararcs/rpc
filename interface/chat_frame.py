import tkinter as tk

class ChatFrame(tk.Frame):
    def __init__(self, master, operation, on_execute):
        super().__init__(master,bg='#cccccc')
        
        self.operation = operation
        self.on_execute = on_execute
        
        # Container principal
        container = tk.Frame(self,bg='#cccccc', bd=1)
        container.pack(padx=40, pady=40)

        # Subtítulo
        subtitle = tk.Label(
            container, text="Digite seu problema matemático e deixe a IA resolver",
            font=('Segoe UI', 15), bg='#cccccc', fg='#666666'
        )
        subtitle.pack(pady=(0, 20))

        # Campo de entrada
        text_frame = tk.Frame(container, bg='#cccccc')
        text_frame.pack(pady=10, padx=30)

        tk.Label(
            text_frame, text="Seu problema:", 
            font=('Segoe UI', 12), bg='#cccccc', fg='#2b2b3c'
        ).pack(anchor='w', pady=(0, 5))

        # Text widget com scrollbar
        text_container = tk.Frame(text_frame,bg='#ffffff', bd=1, relief='solid')
        text_container.pack()

        scrollbar = tk.Scrollbar(text_container)
        scrollbar.pack(side='right', fill='y')

        self.text = tk.Text(
            text_container,
            height=6, width=45,
            font=('Segoe UI', 11), bg='#ffffff',
            fg='#2b2b3c', bd=0, relief='flat', wrap='word',
            yscrollcommand=scrollbar.set,
            insertbackground='#000011',
            padx=10, pady=10
        )
        self.text.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.text.yview)

        # Placeholder
        placeholder = "Ex: Resolva a equação 2x + 5 = 15"
        self.text.insert('1.0', placeholder)
        self.text.config(fg='#999999')

        def on_focus_in(event):
            if self.text.get('1.0', 'end-1c') == placeholder:
                self.text.delete('1.0', 'end')
                self.text.config(fg='#2b2b3c')

        self.text.bind('<FocusIn>', on_focus_in)

        # Botão enviar
        btn = tk.Button(
            container, text="Enviar para IA",
            font=('Segoe UI', 12, 'bold'), bg='#0f172a', fg='#ffffff',
            activebackground='#000011', activeforeground='#ffffff',
            bd=0, cursor='hand2', 
            command=self.execute,
            width=20, pady=12
        )
        btn.pack(pady=(20, 30), padx=30)

        self.output = tk.Label(self,  text="", font=('Segoe UI', 14), bg='#cccccc')
        self.output.pack(pady=20)

        # Efeito hover
        btn.bind('<Enter>', lambda e: btn.config(bg='#000011'))
        btn.bind('<Leave>', lambda e: btn.config(bg='#000011'))

    def get(self):
        text = self.text.get("1.0", "end-1c").strip()
        # Remove o placeholder 
        if text == "Ex: Resolva a equação 2x + 5 = 15":
            return ""
        return text

    def execute(self):
        text = self.get()
        if not text:
            return

        result = self.on_execute(self.operation, text)
        self.show_result(result)

    def show_result(self, result):
        if result is None:
            self.output.config(text="Nenhuma resposta retornada.")
            return

        self.output.config(text=f"Resultado:\n{result}")
