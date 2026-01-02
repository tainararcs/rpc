import tkinter as tk

class HomeFrame(tk.Frame):
    '''
        Frame inicial moderno com boas-vindas e informações do sistema
    '''
    
    def __init__(self, master):
        super().__init__(master, bg='#cccccc')
        
        # Container principal centralizado
        container = tk.Frame(self, bg='#cccccc')
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Subtítulo
        subtitle = tk.Label(
            container,
            text="Sistema integrado de operações matemáticas e inteligência artificial",
            font=('Segoe UI', 13),
            bg='#cccccc', fg='#666666'
        )
        subtitle.pack(pady=(0, 40))
        
        # Cards de features
        features_frame = tk.Frame(container, bg='#cccccc')
        features_frame.pack(pady=(0, 30))
        
        features = [
            ("∑", "Calculadora", "Operações matemáticas básicas"),
            ("!", "Fatorial", "Cálculo de fatoriais"),
            ("✓", "Primos", "Verificação de números primos"),
            ("▤", "Notícias", "Últimas do UOL"),
            ("››", "IA", "Resolvedor inteligente")
        ]
        
        for i, (icon, title_text, desc) in enumerate(features):
            row = i // 3
            col = i % 3
            
            card = tk.Frame(
                features_frame, 
                bg='#ffffff',
                highlightbackground='#e5e7eb',
                highlightthickness=1
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Ícone
            icon_label = tk.Label(
                card, text=icon,
                font=('Segoe UI Emoji', 32),
                bg='#ffffff', fg='#0f172a'
            )
            icon_label.pack(pady=(20, 10))
            
            # Título do card
            card_title = tk.Label(
                card, text=title_text,
                font=('Segoe UI', 12, 'bold'),
                bg='#ffffff', fg='#0f172a'
            )
            card_title.pack()
            
            # Descrição
            card_desc = tk.Label(
                card, text=desc,
                font=('Segoe UI', 9),
                bg='#ffffff', fg='#666666'
            )
            card_desc.pack(pady=(5, 20))
            
            # Largura mínima dos cards
            card.config(width=210, height=150)
            card.pack_propagate(False)
        
        # Instruções
        instructions = tk.Label(
            container,
            text="Selecione uma opção no menu lateral para começar",
            font=('Segoe UI', 12),
            bg='#cccccc', fg='#0f172a'
        )
        instructions.pack(pady=(20, 0))
