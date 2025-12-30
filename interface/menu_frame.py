import server.consts as consts
import tkinter as tk

class MenuFrame(tk.Frame):
    def __init__(self, master, on_select):
        super().__init__(master)
        self.on_select = on_select
        self.current = None

        # Título dinâmico
        self.title_var = tk.StringVar(value="Selecione uma operação")
        title = tk.Label(self, textvariable=self.title_var, font=('Arial', 18, 'bold'))
        title.pack(pady=10)

        # Menu de botões
        menu = tk.Frame(self)
        menu.pack(side='top', fill='x')

        self.buttons = [
            ('Calculadora', consts.CALC),
            ('Fatorial', consts.FAC),
            ('Primo', consts.PRIME),
            ('Notícias UOL', consts.NEWS),
            ('Resolvedor AI', consts.SOLVER),
        ]       

        for text, operation in self.buttons:
            tk.Button(menu, text=text, command=lambda op=operation: self.on_select(op)).pack(fill='x', pady=2)

        # Área dinâmica de conteúdo
        self.content_area = tk.Frame(self)
        self.content_area.pack(fill='both', expand=True, pady=10)

    def show_content(self, frame_cls, title: str, *args):
        self.clear_content()
        self.title_var.set(title)
        self.current = frame_cls(self.content_area, *args)
        self.current.pack(fill='both', expand=True)

    def clear_content(self):
        if self.current:
            self.current.destroy()
            self.current = None
