import tkinter as tk
from tkinter import messagebox

import universal_modloader as uml

from .languages import CURRENT_LANGUAGE, TRANSLATIONS
from .settings_window.gui import open_gui_settings
from .settings_window.language import open_language_settings
from .settings_window.theme import open_theme_settings
from .theme import register_window


@uml.Inject("main", "PyToolsApp.__init__", at=uml.At.TAIL())
def add_mod_menu(ctx):
    self = ctx["self"]

    register_window(self.root)
    self.root.title("PyTool - Ultimate Modded Edition")

    menubar = tk.Menu(self.root)
    self.root.config(menu=menubar)

    mods_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Mod Settings", menu=mods_menu)

    mods_menu.add_command(
        label="GUI",
        command=lambda: open_gui_settings(self.root),
    )
    mods_menu.add_command(
        label="Theme",
        command=lambda: open_theme_settings(self.root),
    )
    mods_menu.add_command(
        label="Language", command=lambda: open_language_settings(self.root)
    )
    mods_menu.add_separator()
    mods_menu.add_command(
        label="About UML",
        command=lambda: messagebox.showinfo("About", "Injected by Universal Modloader"),
    )

    print("[Mod] Menu bar injected successfully.")


@uml.Inject("target_app", at=uml.At.INVOKE("tk.Label"))
@uml.Inject("target_app", at=uml.At.INVOKE("tk.Button"))
@uml.Inject("target_app", at=uml.At.INVOKE("tk.LabelFrame"))
def translate_widget(ctx):
    kwargs = ctx["kwargs"]

    if "text" in kwargs:
        original_text = kwargs["text"]

        trans_dict = TRANSLATIONS.get(CURRENT_LANGUAGE, {})
        if original_text in trans_dict:
            kwargs["text"] = trans_dict[original_text]
