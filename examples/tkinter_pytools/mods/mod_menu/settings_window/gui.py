import tkinter as tk
from tkinter import messagebox, ttk

from .theme import register_window


def open_gui_settings(parent_root):
    settings_win = tk.Toplevel(parent_root)
    settings_win.title("Universal GUI Settings")
    settings_win.geometry("300x250")

    register_window(settings_win)

    x = parent_root.winfo_x() + 50
    y = parent_root.winfo_y() + 50
    settings_win.geometry(f"+{x}+{y}")

    ttk.Label(settings_win, text="Window Opacity (Ghost Mode)").pack(pady=(10, 0))
    opacity_scale = ttk.Scale(
        settings_win,
        from_=0.1,
        to=1.0,
        command=lambda v: parent_root.attributes("-alpha", float(v)),
    )
    opacity_scale.set(parent_root.attributes("-alpha") or 1.0)
    opacity_scale.pack(fill=tk.X, padx=20)

    is_topmost = tk.BooleanVar(value=bool(parent_root.attributes("-topmost")))

    def toggle_topmost():
        parent_root.attributes("-topmost", is_topmost.get())

    ttk.Checkbutton(
        settings_win, text="Always on Top", variable=is_topmost, command=toggle_topmost
    ).pack(pady=10)

    def force_unlock():
        parent_root.resizable(True, True)
        messagebox.showinfo("HACK", "Window Resize UNLOCKED!", parent=settings_win)

    ttk.Button(settings_win, text="Force Unlock Resize", command=force_unlock).pack(
        pady=5
    )

    ttk.Button(settings_win, text="Close", command=settings_win.destroy).pack(pady=20)
