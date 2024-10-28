import re
import tkinter as tk
from typing import Callable

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sympy import Derivative, sympify
from sympy.abc import x

from algorithms import Algorithm
from algorithms_frame import create_button_frame
from const import BACKGROUND_COLOR
from input_frame import create_input_frame
from lib import (bisection, modified_newtons, newtons, normalize_equation,
                 regula_falsi, secant)
from table_frame import create_table
from tutorial_frame import create_tutorial

mode = Algorithm.BISECTION

def update_canvas(figure):
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=0, padx=5, pady=5, sticky='NESW')


def on_press(algorithm: Algorithm):
    global mode
    mode = algorithm
    frame = window.nametowidget("algorithms_frame")
    window.nametowidget('input_frame.execute_btn').configure(state='normal')

    for widget in frame.winfo_children():
        widget.configure(bg='#50577A', fg='#FFFFFF')

    if algorithm == Algorithm.BISECTION:
        window.nametowidget("algorithms_frame.bisect").configure(bg='#ECB365', fg='#000000')
    elif algorithm == Algorithm.SECANT:
        window.nametowidget("algorithms_frame.secant").configure(bg='#ECB365', fg='#000000')
    elif algorithm == Algorithm.REGULA_FALSI:
        window.nametowidget("algorithms_frame.regula_falsi").configure(bg='#ECB365', fg='#000000')
    elif algorithm == Algorithm.NEWTONS:
        window.nametowidget("algorithms_frame.newtons").configure(bg='#ECB365', fg='#000000')
    elif algorithm == Algorithm.MODIFIED_NEWTONS:
        window.nametowidget("algorithms_frame.modified_newtons").configure(bg='#ECB365', fg='#000000')

    upper_bound = window.nametowidget('input_frame.upper_bound_input')
    upper_bound.configure(state='normal')

    if algorithm in [Algorithm.NEWTONS, Algorithm.MODIFIED_NEWTONS]:
        upper_bound.configure(state='disabled')

def on_execute():
    global mode
    equation, x0_input, x1_input, tolerance = get_input()
    equation = normalize_equation(equation)

    f = sympify(equation)
    graphable = None

    if mode == Algorithm.BISECTION:
        graphable = bisection(f, x0_input, x1_input, tolerance)
    elif mode == Algorithm.SECANT:
        graphable = secant(f, x0_input, x1_input, tolerance)
    elif mode == Algorithm.REGULA_FALSI:
        graphable = regula_falsi(f, x0_input, x1_input, tolerance)
    elif mode == Algorithm.NEWTONS:
        df = Derivative(f)
        graphable = newtons(f, df, x0_input, tolerance)
    elif mode == Algorithm.MODIFIED_NEWTONS:
        df = Derivative(f)
        graphable = modified_newtons(f, df, x0_input, tolerance)

    figure = Figure()
    print(graphable.additional_cols)
    plot = figure.add_subplot(1, 1, 1)
    x2 = np.linspace(-4, 4, 500)
    y2 = list(map(lambda x_val: f.subs(x, x_val).doit(), x2))
    plot.plot(x2, y2, 'c')

    plot.plot(graphable.x_arr[:graphable.starter_vals], graphable.y_arr[:graphable.starter_vals], 'go')
    plot.plot(graphable.x_arr[graphable.starter_vals:-1], graphable.y_arr[graphable.starter_vals:-1], 'mo')
    plot.plot(graphable.x_arr[-1:], graphable.y_arr[-1:], 'bo')
    graphable.annotate(plot)

    update_canvas(figure)

    create_table(window, graphable).grid(row=1, column=1, rowspan=2, sticky='NESW', padx=5, pady=5)



def get_input():

    global mode
    formula = window.nametowidget("input_frame.equation_input").get()
    x0 = float(window.nametowidget("input_frame.lower_bound_input").get())

    if mode == Algorithm.BISECTION or mode == Algorithm.SECANT or mode == Algorithm.REGULA_FALSI:
        x1 = float(window.nametowidget("input_frame.upper_bound_input").get())
    else:
        x1 = float(0)

    tolerance = float(window.nametowidget("input_frame.tolerance_input").get())


    return formula, x0, x1, tolerance


window = tk.Tk()
window.configure(bg=BACKGROUND_COLOR)
window.title('Numericko rjesavanje nelinearnih jednacina')
window.geometry('1280x720')

create_button_frame(window, on_press).grid(row=0, column=0, columnspan=2)
window.grid_columnconfigure(0, weight=1, uniform='uwu')
window.grid_columnconfigure(1, weight=1, uniform='uwu')

create_input_frame(window, on_execute).grid(row=1, column=0, sticky='EW')

create_tutorial(window).grid(row=1, column=1, rowspan=2, sticky='NESW')

figure = Figure(figsize=(6, 4), dpi=100)
axes = figure.add_subplot()
update_canvas(figure)

window.mainloop()

