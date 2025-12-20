import tkinter as tk
from tkinter import ttk

from ..languages import CURRENT_LANGUAGE, TRANSLATIONS, switch_global_language
from .theme import register_window


def open_language_settings(parent_root):
    lang_win = tk.Toplevel(parent_root)
    lang_win.title("Language Settings")
    lang_win.geometry("250x300")

    register_window(lang_win)

    ttk.Label(lang_win, text="Select Language:").pack(pady=10)

    frame = ttk.Frame(lang_win)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    listbox = tk.Listbox(frame, font=("Helvetica", 11), height=10)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for i, lang in enumerate(TRANSLATIONS.keys()):
        listbox.insert(tk.END, lang)
        if lang == CURRENT_LANGUAGE:
            listbox.selection_set(i)
            listbox.activate(i)

    def on_select(event):
        sel = listbox.curselection()
        if not sel:
            return
        lang = listbox.get(sel[0])

        switch_global_language(lang)

    listbox.bind("<<ListboxSelect>>", on_select)
    ttk.Button(lang_win, text="Close", command=lang_win.destroy).pack(pady=10)
