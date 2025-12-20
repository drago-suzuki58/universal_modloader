import tkinter as tk
from tkinter import ttk

from ..theme import (
    CURRENT_THEME_NAME,
    CUSTOM_THEMES,
    register_window,
    switch_global_theme,
)


def open_theme_settings(parent_root):
    theme_win = tk.Toplevel(parent_root)
    theme_win.title("Theme Injector")
    theme_win.geometry("250x350")

    register_window(theme_win)

    ttk.Label(theme_win, text="Select Color Scheme:").pack(pady=10)

    frame = ttk.Frame(theme_win)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    listbox = tk.Listbox(frame, font=("Helvetica", 11), height=10)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for i, t in enumerate(CUSTOM_THEMES.keys()):
        listbox.insert(tk.END, t)
        if t == CURRENT_THEME_NAME:
            listbox.selection_set(i)
            listbox.activate(i)

    def on_select(event):
        sel = listbox.curselection()
        if not sel:
            return
        name = listbox.get(sel[0])

        switch_global_theme(name)

    listbox.bind("<<ListboxSelect>>", on_select)
    ttk.Button(theme_win, text="Close", command=theme_win.destroy).pack(pady=10)
