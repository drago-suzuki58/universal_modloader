from tkinter import ttk

CUSTOM_THEMES = {
    "Standard (Default)": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "entry_bg": "#ffffff",
        "entry_fg": "#000000",
        "select_bg": "#0078d7",
        "base_theme": "default",
    },
    "Dark Mode": {
        "bg": "#2b2b2b",
        "fg": "#ffffff",
        "entry_bg": "#3c3f41",
        "entry_fg": "#ffffff",
        "select_bg": "#4b6eaf",
        "base_theme": "clam",
    },
    "Hacker Green": {
        "bg": "#0d0d0d",
        "fg": "#00ff00",
        "entry_bg": "#1a1a1a",
        "entry_fg": "#00ff00",
        "select_bg": "#003300",
        "base_theme": "alt",
    },
    "Solarized Light": {
        "bg": "#fdf6e3",
        "fg": "#586e75",
        "entry_bg": "#eee8d5",
        "entry_fg": "#586e75",
        "select_bg": "#93a1a1",
        "base_theme": "clam",
    },
    "Deep Blue": {
        "bg": "#001f3f",
        "fg": "#7FDBFF",
        "entry_bg": "#00152b",
        "entry_fg": "#7FDBFF",
        "select_bg": "#0074D9",
        "base_theme": "clam",
    },
}

CURRENT_THEME_NAME = "Standard (Default)"
ACTIVE_WINDOWS = set()


def register_window(win):
    ACTIVE_WINDOWS.add(win)

    def on_close():
        if win in ACTIVE_WINDOWS:
            ACTIVE_WINDOWS.remove(win)
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)

    apply_theme_to_window(win, CURRENT_THEME_NAME)


def switch_global_theme(theme_name):
    global CURRENT_THEME_NAME
    if theme_name not in CUSTOM_THEMES:
        return

    CURRENT_THEME_NAME = theme_name
    print(f"[Mod] Global theme switch: {theme_name}")

    for win in list(ACTIVE_WINDOWS):
        try:
            if win.winfo_exists():
                apply_theme_to_window(win, theme_name)
        except Exception:
            pass


def apply_theme_to_window(root, theme_name):
    colors = CUSTOM_THEMES[theme_name]
    style = ttk.Style()

    try:
        if style.theme_use() != colors["base_theme"]:
            style.theme_use(colors["base_theme"])
    except Exception:
        pass

    style.configure(
        ".",
        background=colors["bg"],
        foreground=colors["fg"],
        fieldbackground=colors["entry_bg"],
    )
    style.configure("TLabel", background=colors["bg"], foreground=colors["fg"])
    style.configure("TButton", background=colors["bg"], foreground=colors["fg"])
    style.map("TButton", background=[("active", colors["select_bg"])])

    try:
        root.configure(bg=colors["bg"])
    except Exception:
        pass

    def force_paint(widget):
        try:
            w_class = widget.winfo_class()

            if w_class in (
                "Frame",
                "Labelframe",
                "Toplevel",
                "Tk",
                "Canvas",
                "Label",
                "Button",
                "Message",
                "Checkbutton",
                "Radiobutton",
            ):
                widget.configure(bg=colors["bg"])
                if w_class not in ("Frame", "Labelframe", "Toplevel", "Tk", "Canvas"):
                    widget.configure(fg=colors["fg"])
                    if w_class in ("Checkbutton", "Radiobutton"):
                        widget.configure(
                            activebackground=colors["bg"],
                            activeforeground=colors["fg"],
                            selectcolor=colors["entry_bg"],
                        )

            if w_class in ("Text", "Entry", "Listbox", "Spinbox"):
                widget.configure(
                    bg=colors["entry_bg"],
                    fg=colors["entry_fg"],
                    insertbackground=colors["fg"],
                    selectbackground=colors["select_bg"],
                    selectforeground=colors["select_fg"],
                )

            for child in widget.winfo_children():
                force_paint(child)

        except Exception:
            pass

    force_paint(root)
