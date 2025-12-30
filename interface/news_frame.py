# interface/output_frame.py
import tkinter as tk

class NewsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side='right', fill='y')

        self.text = tk.Text(self, wrap='word', yscrollcommand=scrollbar.set, font=('Arial', 12))
        self.text.pack(fill='both', expand=True)

        scrollbar.config(command=self.text.yview)

    def set_text(self, content: str):
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, content)
