# tkinter_pytools

[日本語](./examples/tkinter_pytools/README.ja.md) | English

This example demonstrates a complete **GUI Overhaul**. It shows how to inject modern UI features, theming, and localization into a legacy Tkinter application at runtime, transforming a rigid tool into a flexible one.

## The Target

A collection of developer utilities (Text Analyzer, Hash Gen, Epoch Converter, UUID Gen) built with standard Tkinter.

It represents a typical "legacy" internal tool.

- **Stack:** Tkinter (Standard Library).
- **Behavior:**
  - **Rigid Window:** The window size is fixed (non-resizable).
  - **Boring UI:** Uses the default, gray, OS-native look.
  - **Hardcoded Text:** All labels and buttons are hardcoded in English.
  - **Limited UX:** Lacks convenience features like "Copy to Clipboard" for generated hashes.

## The Mod

The Mods inject a new menu bar to control the application's appearance and behavior, effectively rewriting the UI layer.

- **Mod Menu Injection (mod_menu.py):**
  - **Menu Bar:** Injects a "Mods" menu bar into the main window (which originally had none).
  - **Theme Selector:** Allows dynamic switching between color palettes (Dark Mode, Hacker Green, etc.) to change the UI appearance.
  - **Runtime Localization:** Switches the entire UI language (English/Japanese/German) on the fly by intercepting widget creation and text updates.
  - **Window Control:** Adds settings to toggle "Always on Top", adjust window opacity (Alpha), and force-unlock window resizing.
- **UX Improvement (hash_copy.py):**
  - Uses an overlay technique (`place`) to inject a "Copy" button directly on top of existing labels in the Hash Generator, adding missing functionality without breaking the layout.

| Before (Original) | After (Modded) |
| :---: | :---: |
| <img src="./examples/tkinter_pytools/before.png" width="400"> | <img src="./examples/tkinter_pytools/after.png" width="400"> |

## How to Run

### Prerequisite

Ensure you have `uv` installed and dependencies synced.

### 1. Run Modded (Modernized)

The loader injects the UI overhaul mods.

```bash
cd examples/tkinter_pytools
# Run the target via the Universal Modloader
uv run loader.py
```

**Try this:**  
1. Try disabling window resizing from **Mod Settings > GUI** and resizing it (it is now unlocked).
2. Use the **Mods > Theme Selector** menu to change the look (e.g., to "Hacker Green").
3. Use the **Mods > Language Settings** menu to switch to Japanese or German.
4. Generate a hash and use the injected **[Copy]** button.

### 2. Run Vanilla (Legacy)

Verify the original rigid behavior.

```bash
cd examples/tkinter_pytools
uv run main.py
```

**Try this:**  
Try to resize the window (you can't). Look for the Mods menu (it's gone).
