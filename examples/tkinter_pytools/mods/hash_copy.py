import tkinter as tk

import universal_modloader as uml


@uml.Inject("main", "PyToolsApp._build_hash_generator", at=uml.At.TAIL())
def add_hash_copy_buttons(ctx):
    app = ctx["self"]

    def copy_from_label(label_widget, btn_widget):
        full_text = label_widget.cget("text")
        if ":" in full_text:
            hash_val = full_text.split(":", 1)[1].strip()

            if not hash_val or hash_val in ["-", "(未計算)", "(Ausstehend)"]:
                print("[Mod] Nothing to copy.")
                original_text = btn_widget.cget("text")

                btn_widget.configure(text="Empty!")
                btn_widget.after(1000, lambda: btn_widget.configure(text=original_text))
                return

            app.root.clipboard_clear()
            app.root.clipboard_append(hash_val)
            print(f"[Mod] Copied to clipboard: {hash_val}")

            btn_widget.configure(text="Copied!")

            def reset_btn():
                btn_widget.configure(text="Copy")

            btn_widget.after(1000, reset_btn)

    def create_overlay_button(target_label):
        parent = target_label.master

        btn = tk.Button(parent, text="Copy", font=("Arial", 8), cursor="hand2")
        btn.configure(text="Copy Hash")
        btn.configure(command=lambda: copy_from_label(target_label, btn))
        btn.place(in_=target_label, relx=1.0, x=-4, rely=0.5, anchor="e", height=24)

        return btn

    create_overlay_button(app.md5_label)
    create_overlay_button(app.sha_label)

    print("[Mod] Injected 'Copy' buttons into Hash Generator.")
