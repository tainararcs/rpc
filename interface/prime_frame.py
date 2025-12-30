import tkinter as tk

# usuário digita → clica Calcular → callback → RPC → resultado

class PrimeFrame(tk.Frame):
    def __init__(self, master, operation, on_execute):
        super().__init__(master)

        self.operation = operation
        self.on_execute = on_execute

        tk.Label(self, text="Números (separados por vírgula):").pack()
        self.entry = tk.Entry(self, width=40)
        self.entry.pack()

        tk.Button(self, text="Verificar", command=self.execute).pack()

    def execute(self):
        value = self.entry.get().strip()
        self.on_execute(self.operation, value)
