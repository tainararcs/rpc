from tkinter import messagebox
import server.consts as consts
from operations import Operations
from interface.prime_frame import PrimeFrame
from interface.menu_frame import MenuFrame
from interface.calculator_frame import CalculatorFrame
from interface.factoial_frame import FactorialFrame
from interface.chat_frame import ChatFrame
from interface.news_frame import NewsFrame
import tkinter as tk

CALC_OPS = {consts.CALC, consts.SUM, consts.SUB, consts.MUL, consts.DIV}
FAC_OPS = {consts.FAC}
PRIME_OPS = {consts.PRIME}
CHAT_OPS = {consts.SOLVER}
NO_INPUT_OPS = {consts.NEWS}

TITLES = {
    consts.CALC: "Calculadora",
    consts.FAC: "Fatorial",
    consts.PRIME: "Número Primo",
    consts.NEWS: "Notícias UOL",
    consts.SOLVER: "Resolvedor com IA",
}

def create_interface():
    window = tk.Tk()
    window.title('Remote Procedure Call')
    window.geometry('1200x800')
    return window

def manage_interface_rpc(window, op: Operations, on_execute):

    def on_operation_selected(operation):
        title = TITLES.get(operation, "Operação")

        if operation in CALC_OPS:
            frame_menu.show_content(CalculatorFrame, title, on_execute)
        elif operation in FAC_OPS:
            frame_menu.show_content(FactorialFrame, title, operation, on_execute)
        elif operation in PRIME_OPS:
            frame_menu.show_content(PrimeFrame, title, operation, on_execute)
        elif operation in CHAT_OPS:
            frame_menu.show_content(ChatFrame, title, operation, on_execute)
        elif operation in NO_INPUT_OPS:
            frame_menu.show_content(NewsFrame, title)
            result = on_execute(operation, None)
            frame_menu.current.set_text(result)

    tk.Label(window, text='Operações RPC', font=('Arial', 16)).pack(pady=10)

    frame_menu = MenuFrame(window, on_select=on_operation_selected)
    frame_menu.pack(fill='both', expand=True)
