from server import consts
import tkinter as tk

class CalculatorFrame(tk.Frame):
    def __init__(self, master, on_execute):
        super().__init__(master, bg='#cccccc')
        
        self.on_execute = on_execute
        
        self.current = ""
        self.numbers = []
        self.operator = None

        # Container da calculadora com borda
        calc_container = tk.Frame(self, bg='#cccccc', relief='solid', bd=1)
        calc_container.pack(padx=20, pady=20)

        # Display
        self.display = tk.Entry(
            calc_container, font=('Segoe UI', 24, 'bold'), justify='right',
            width=15, bg='#2b2b3c', fg='#ffffff',
            bd=0, relief='flat', insertbackground='#0f172a'
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=15)

        self.buttons = [
            ('C', 1, 0, '#ff6b6b', '#ffffff'),
            ('7', 2, 0, '#ffffff', '#2b2b3c'), ('8', 2, 1, '#ffffff', '#2b2b3c'), 
            ('9', 2, 2, '#ffffff', '#2b2b3c'), ('/', 2, 3, '#0f172a', '#ffffff'),
            ('4', 3, 0, '#ffffff', '#2b2b3c'), ('5', 3, 1, '#ffffff', '#2b2b3c'), 
            ('6', 3, 2, '#ffffff', '#2b2b3c'), ('*', 3, 3, '#0f172a', '#ffffff'),
            ('1', 4, 0, '#ffffff', '#2b2b3c'), ('2', 4, 1, '#ffffff', '#2b2b3c'), 
            ('3', 4, 2, '#ffffff', '#2b2b3c'), ('-', 4, 3, '#0f172a', '#ffffff'),
            ('0', 5, 0, '#ffffff', '#2b2b3c'), ('.', 5, 1, '#ffffff', '#2b2b3c'), 
            ('=', 5, 2, '#4ade80', '#ffffff'), ('+', 5, 3, '#0f172a', '#ffffff'),
        ]

        self.OP_MAP = {
            '+': consts.SUM,
            '-': consts.SUB,
            '*': consts.MUL,
            '/': consts.DIV,
        }

        for text, row, col, bg_color, fg_color in self.buttons:
            btn = tk.Button(
                calc_container, text=text, font=('Segoe UI', 16, 'bold'), width=5,
                height=2, bg=bg_color, fg=fg_color,
                activebackground=bg_color,
                activeforeground=fg_color,
                bd=0, relief='flat', cursor='hand2',
                command=lambda t=text: self.on_click(t)
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            # Efeito hover
            def on_enter(e, button=btn, color=bg_color):
                brightness = 0.9 if color == '#ffffff' else 1.1
                button.config(bg=self.adjust_color(color, brightness))
            
            def on_leave(e, button=btn, color=bg_color):
                button.config(bg=color)

            self.output = tk.Label(self,  text="", font=('Segoe UI', 14), bg='#cccccc')
            self.output.pack(pady=20)
            
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
    
    def adjust_color(self, hex_color, factor):
        '''
            Ajusta o brilho de uma cor hexadecimal
        '''
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, max(0, int(r * factor)))
        g = min(255, max(0, int(g * factor)))
        b = min(255, max(0, int(b * factor)))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def on_click(self, char: str):
        if char == 'C':
            self.clear()
            return

        if char == '=':
            if not self.operator or not self.current:
                return

            self.numbers.append(self.current)
            operation = self.OP_MAP[self.operator]

            result = self.on_execute(operation, *self.numbers)
            self.output.config(text=f"Resultado: {result}")

            self.clear(keep_result=result)
            return


        if char in self.OP_MAP:
            if not self.current:
                return

            self.numbers.append(self.current)
            self.current = ""
            self.operator = char
            self.display.delete(0, tk.END)
            return

        if char == '.':
            if '.' in self.current:
                return
            if self.current == "":
                self.current = "0."
                self.display.insert(tk.END, "0.")
            else:
                self.current += '.'
                self.display.insert(tk.END, '.')
            return

        if char.isdigit():
            self.current += char
            self.display.insert(tk.END, char)

    def clear(self, keep_result=None):
        self.current = ""
        self.numbers.clear()
        self.operator = None
        self.display.delete(0, tk.END)

        if keep_result is not None:
            self.current = str(keep_result)
            self.display.insert(0, self.current)
