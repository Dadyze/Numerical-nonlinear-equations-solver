import tkinter as tk

from const import BACKGROUND_COLOR, TEXT_COLOR


def create_input_frame(container, callback):
    frame = tk.Frame(container, bg=BACKGROUND_COLOR, name='input_frame')
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)
    
    equation_label = tk.Label(frame, text='Jednačina:', bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    equation_input = tk.Entry(frame, fg="#F1F1F4", bg="#6B728E", borderwidth=0, name='equation_input')
    equation_label.grid(row=0, column=0, columnspan=3, sticky="W")
    equation_input.grid(row=1, column=0, columnspan=3, sticky='EW')

    lower_bound_label = tk.Label(frame, text='Početna tačka:', bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    lower_bound_input = tk.Entry(frame, fg="#F1F1F4", bg="#6B728E", borderwidth=0, name='lower_bound_input')
    lower_bound_label.grid(row=2, column=0, sticky="W")
    lower_bound_input.grid(row=3, column=0, sticky='EW')

    upper_bound_label = tk.Label(frame, text='Krajnja tačka:', bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    upper_bound_input = tk.Entry(frame, fg="#F1F1F4", bg="#6B728E", disabledbackground="#53576F", borderwidth=0, name='upper_bound_input')
    upper_bound_label.grid(row=2, column=1, sticky="W")
    upper_bound_input.grid(row=3, column=1, sticky='EW')

    tolerance_label = tk.Label(frame, text='Tačnost:', bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    tolerance_input = tk.Entry(frame, textvariable=tk.StringVar(value='1e-5'), fg="#F1F1F4", bg="#6B728E", borderwidth=0, name='tolerance_input')
    tolerance_label.grid(row=2, column=2, sticky="W")
    tolerance_input.grid(row=3, column=2, sticky='EW')

    button = tk.Button(
        frame,
        command=callback,
        height=2,
        width=28,
        text='Izračunaj',
        bg='#ECB365',
        fg='#000000',
        activebackground='#6B728E',
        activeforeground='#FFFFFF',
        borderwidth=0,
        state='disabled',
        name='execute_btn'
    )

    button.grid(row=4, column=0, columnspan=3)
    for widget in frame.winfo_children():
        widget.grid(padx=5, pady=5)

    return frame

