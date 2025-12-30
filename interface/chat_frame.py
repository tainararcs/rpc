import tkinter as tk

# usuário digita → clica Enviar → callback → RPC → resultado

class ChatFrame(tk.Frame):
    def __init__(self, master, operation, on_execute):
        super().__init__(master)
        self.text = tk.Text(self, height=5, width=40)
        self.text.pack()
        self.button = tk.Button(self, text="Enviar", command=lambda: on_execute(operation, self.get()))
        self.button.pack()

    def get(self):
        return self.text.get("1.0", "end").strip()

    def execute(self):
        text = self.textbox.get("1.0", tk.END).strip()
        self.on_execute(self.operation, text)
