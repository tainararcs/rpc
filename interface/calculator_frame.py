from server import consts
import tkinter as tk

class CalculatorFrame(tk.Frame):
    def __init__(self, master, on_execute):
        super().__init__(master)
        
        self.on_execute = on_execute
        
        self.current = ""        # número sendo digitado (string)
        self.numbers = []        # lista de números completos (strings)
        self.operator = None

        self.display = tk.Entry(self, font=('Arial', 18), justify='right', width=15)
        self.display.grid(row=0, column=0, columnspan=4, pady=10)

        self.buttons = [
            ('C', 1, 0), 
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3),
        ]

        self.OP_MAP = {
            '+': consts.SUM,
            '-': consts.SUB,
            '*': consts.MUL,
            '/': consts.DIV,
        }

        for text, row, col in self.buttons:
            tk.Button(self, text=text, font=('Arial', 14), width=5, height=2, command=lambda t=text: self.on_click(t)).grid(row=row, column=col, padx=5, pady=5)
    
    def get(self):
        return self.entry.get()
    
    def on_click(self, char: str):
        if char == 'C':
            self.clear()
            return

        if char == '=':
            if not self.operator or not self.current:
                return

            self.numbers.append(self.current)
            operation = self.OP_MAP[self.operator]
            self.on_execute(operation, *self.numbers)
            self.clear()
            return

        # Operador
        if char in self.OP_MAP:
            if not self.current:
                return

            self.numbers.append(self.current)
            self.current = ""
            self.operator = char
            self.display.delete(0, tk.END)
            return

        # Número decimal
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
  

    def execute(self):
        operation = self.OP_MAP[self.operator]

        self.on_execute(operation, *self.numbers)
        self.clear()

    def clear(self):
        self.current = ""
        self.numbers.clear()
        self.operator = None
        self.display.delete(0, tk.END)
        