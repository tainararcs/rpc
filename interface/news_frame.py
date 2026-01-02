'''
    Frame responsável pela exibição de notícias retornadas pelo servidor RPC.
'''
import tkinter as tk

class NewsFrame(tk.Frame):
    '''
        Frame de visualização de notícias com scroll.
    '''
    def __init__(self, master: tk.Widget) -> None:
        '''
            Inicializa o frame de notícias.
        '''
        super().__init__(master, bg='#cccccc')

        # Card central
        card = tk.Frame(self, bg='#ffffff')
        card.pack(fill='x', padx=35, pady=20)

        # Título
        title = tk.Label(
            card,
            text="Notícias", font=('Segoe UI', 18, 'bold'),
            bg='#ffffff', fg='#0f172a'
        )
        title.pack(anchor='w', padx=20, pady=(15, 10))

        # Separador
        separator = tk.Frame(card, bg='#e5e7eb', height=1)
        separator.pack(fill='x', padx=20, pady=(0, 10))

        # Container do texto com scroll
        text_container = tk.Frame(card, bg='#ffffff')
        text_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        scrollbar = tk.Scrollbar(text_container)
        scrollbar.pack(side='right', fill='y')

        self.text = tk.Text(
            text_container,
            wrap='word',
            yscrollcommand=scrollbar.set,
            font=('Segoe UI', 12), bg='#ffffff', fg='#111827',
            bd=0, highlightthickness=0, padx=10, pady=10
        )
        self.text.pack(fill='both', expand=True)

        scrollbar.config(command=self.text.yview)

        # Texto somente leitura
        self.text.config(state='disabled')

    def set_text(self, content: str):
        '''
            Atualiza o conteúdo textual exibido.

            Args:
                content (str): Texto a ser exibido.
        '''
        self.text.config(state='normal')
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, content)
        self.text.config(state='disabled')
