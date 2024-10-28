import tkinter as tk
from typing import Callable

from algorithms import Algorithm
from const import BACKGROUND_COLOR, TEXT_COLOR

counter = 0

def register_algorithm(container, name: str, callback: Callable, id: str):

    global counter

    button = tk.Button(
        container,
        command=callback,
        height=2,
        width=19,
        text=name,
        bg="#50577A",
        fg=TEXT_COLOR,
        activebackground="#ECB365",
        borderwidth=0,
        name=id
    )

    
    button.grid(row=0, column=counter)
    counter += 1


def create_button_frame(container, on_press):
    frame = tk.Frame(container, bg=BACKGROUND_COLOR, name='algorithms_frame')

    register_algorithm(frame, 'Bisekcija', lambda: on_press(Algorithm.BISECTION), 'bisect')
    register_algorithm(frame, 'Regula Falsi', lambda: on_press(Algorithm.REGULA_FALSI), 'regula_falsi')
    register_algorithm(frame, 'Sekanta', lambda: on_press(Algorithm.SECANT), 'secant')
    register_algorithm(frame, 'Newton', lambda: on_press(Algorithm.NEWTONS), 'newtons')
    register_algorithm(frame, 'Modifikovani Newton', lambda: on_press(Algorithm.MODIFIED_NEWTONS), 'modified_newtons')

    for widget in frame.winfo_children():
        widget.grid(padx=5, pady=5)

    return frame

