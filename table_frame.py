import tkinter as tk
from tkinter import ttk

from const import BACKGROUND_COLOR, TEXT_COLOR
from lib import Graphable


def create_table(container, graphable: Graphable):
    
    frame = tk.Frame(container, bg=BACKGROUND_COLOR)

    if graphable == None:
        return frame

    columns = ['Iteracija']

    for key in graphable.additional_cols.keys():
        columns.append(key)

    columns.append('X')
    columns.append('f(X)')
    columns.append('Greska')

    tree = ttk.Treeview(frame, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.column('Iteracija', width=60, stretch=False)
    
    iter = 1
    deltas = graphable.deltas()
    starter_vals = graphable.starter_vals
    for i in range(len(graphable.x_arr)-starter_vals):
        row =[iter]

        for val in graphable.additional_cols.values():
            row.append(val[i])

        row.append(graphable.x_arr[i+starter_vals])
        row.append(graphable.y_arr[i+starter_vals])
        row.append(deltas[i])
        tree.insert('', tk.END, values=row)

        iter += 1


    tree.pack(fill='both', expand=True)
    return frame