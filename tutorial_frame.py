import tkinter as tk

from const import BACKGROUND_COLOR, TEXT_COLOR


def create_tutorial(container):
    
    frame = tk.Frame(container, bg=BACKGROUND_COLOR)
    tutorial_text = tk.Label(frame, text='Aplikacija za numeričko rješavanje nelinearnih jednačina.\nOdaberite metodu za koju želite riješiti jednačinu te popunite odgovarajuće podatke. Za proračun rezultata kliknite dugme "Izračunaj".\n\nLegenda za grafikon:\n\n-ZELENA: početne tačke;\n-ROZA: vrijednosti iteracija;\n-PLAVA: nula.', bg=BACKGROUND_COLOR, fg=TEXT_COLOR, wraplength=250, justify='center')
    tutorial_text.place(relx=0.5, rely=0.5, anchor= 'center')

    
    return frame