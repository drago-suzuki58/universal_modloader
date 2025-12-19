# Universal Modloader (UML)

[![Status](https://img.shields.io/badge/status-Alpha-orange)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

[日本語](README.ja.md) | English

**A Mixin/Harmony-style modding framework for Python using AST injection.**

Universal Modloader is not just a simple plugin loader.

It parses the source code of the target application (and its libraries) at runtime, injects code directly into the **Abstract Syntax Tree (AST)**, and rebuilds it.

This allows you to modify function logic and **access/rewrite local variables** safely via simple decorators, without editing original source files.

> [!WARNING]
> **Alpha Version / Experimental Technical Preview**
>
> This project is currently in **Alpha**. It serves as a **Proof of Concept** exploring the limits of Python's dynamic nature.
>
> By design, this tool utilizes **Runtime AST Injection** to bypass standard safety mechanisms (such as scope and immutability) to enable "impossible" modifications.
>
> **Not intended for production use.**
>
> This tool prioritizes **Power and Flexibility** over Safety and Stability. APIs and internal structures are subject to change without notice. Please treat this as a research tool or a modding framework, not as a standard dependency.

## Features

- **Runtime AST Injection:**  
  No need to overwrite `.py` files. All modifications take place in memory.
- **Local Variable Manipulation:**  
  Access and modify variables inside functions using the `ctx` object.
- **Decorator-based API:**  
  Simple and intuitive syntax inspired by Java's Mixin and C#'s Harmony (Unity).
- **High Versatility:**  
  Can hook into not only the main script but also imported libraries (standard libraries or 3rd party packages).

## Usage Examples

### HEAD

Injects code at the **start** of the function.
This is useful for modifying arguments or local variables before the main logic runs.

**Target Code (`main.py`)**

```python
def take_damage(amount):
    print(f"Ouch! Took {amount} damage.")
```

**Mod Code (`mods/my_mod.py` or `mods/my_mod/__init__.py`)**

```python
@uml.Inject("main", "take_damage", at=uml.At.HEAD())
def on_take_damage(ctx):
    # Overwrite the local variable 'amount' before it is used
    print("[Mod] Nullifying damage!")
    ctx["amount"] = 0
```

### TAIL

Injects code at the **end** of the function (before the return).
Useful for logging or reading the final state of variables.

**Target Code (`main.py`)**

```python
def heal_player():
    hp = 100
    print("Player healed.")
```

**Mod Code (`mods/my_mod.py` or `mods/my_mod/__init__.py`)**

```python
@uml.Inject("main", "heal_player", at=uml.At.TAIL())
def on_heal_player(ctx):
    # Read the local variable 'hp'
    current_hp = ctx["hp"]
    print(f"[Mod] Player HP is now: {current_hp}")
```

### RETURN

Injects code to override the return value.

**Target Code (`main.py`)**

```python
def calculate_damage():
    return random.randint(5, 15)
```

**Mod Code (`mods/my_mod.py` or `mods/my_mod/__init__.py`)**

```python
import universal_modloader as uml

@uml.Inject("main", "calculate_damage", at=uml.At.RETURN())
def on_calculate_damage(ctx):
    print("[Mod] System: Damage calculation overridden!")
    # Setting "__return__" forces the function to return this value
    ctx["__return__"] = 0
```

In this case, `__return__` forces an overwrite of the original return value, so `0` is returned instead of the random integer.

### INVOKE

Intercepts a specific **function call** inside the target function.

This is powerful for modifying arguments passed to a function *before* it executes, or changing its return value *after* it returns.

**Target Code (`main.py`)**

```python
def main():
    # The mod wants to change this name "Hero"
    player = Player("Hero")
    print(f"Welcome, {player.name}!")
```

**Mod Code (`mods/my_mod.py` or `mods/my_mod/__init__.py`)**

```python
CUSTOM_NAME = "ModdedHero"

# Hooks the 'Player(...)' call inside the 'main' function
@uml.Inject("main", "main", at=uml.At.INVOKE("Player"))
def on_create_player(ctx):
    # ctx['args'] is a list of positional arguments passed to Player()
    original_name = ctx['args'][0]
    
    # Overwrite the argument
    ctx['args'][0] = CUSTOM_NAME
    print(f"[Mod] Player name changed from '{original_name}' to '{CUSTOM_NAME}'")
```

By default, `INVOKE` triggers **before** the function is called, allowing argument modification. You can also use `shift=uml.Shift.AFTER` to modify the return value.

## Installation & Usage

To install mods for a game or application:

1. Copy the `mods` folder and `loader.py` from this repository into the target application's folder.
2. Run `loader.py` using Python.

### Basic Usage

By default, the loader attempts to launch `main.py`.

```bash
python loader.py
```

### Advanced Usage

You can specify a different target script or pass arguments to the game itself.

**Syntax:**

```bash
python loader.py [target_script] [game_arguments...]
```

**Examples:**
- **Launch a specific script:**
    ```bash
    python loader.py my_game.py
    ```
    *Note: When loading `my_game.py`, the target module name for `@Inject` becomes `"my_game"` instead of `"main"`.*

- **Pass arguments to the game:**
    ```bash
    python loader.py main.py --debug --windowed
    ```
    *(The arguments `--debug --windowed` are passed directly to `main.py`)*

## How to Run Examples

The applications in the `examples` folder do not have mods installed by default upon cloning.

You can install them using the method described above, or simply run the initialization script to automatically install mods for all examples:

- **Windows:** `initialize.bat`
- **Linux/Mac:** `initialize.sh`

## Roadmap / TODO

### Core Features (Modding System)

- [x] **Injection Points**
  - [x] `HEAD` (Start of function)
  - [x] `TAIL` (End of function)
  - [x] `RETURN` (Rewrite return value)
  - [x] `INVOKE` (Before/After specific function calls)
- [ ] **Mod Metadata (Manifest)**: Support for `__manifest__` dict or `manifest.json` to define name, version, author, and description.
- [ ] **Mod Load Order / Priority**: Ability to define the order in which mods are applied (e.g., using integer priority or "load_after" directive).
- [ ] **Dependency Management**: Define prerequisite mods and ensure they are loaded first.
- [ ] **Library Management**: Automatically install required PyPI packages defined by mods (e.g., `requirements.txt` or `pyproject.toml` per mod).
- [ ] **Conflict Detection**: Warn when multiple mods try to hijack the same function/variable in conflicting ways.

### Developer Experience (DX)

- [ ] **Configuration API**: A standard way for mods to save/load settings (JSON/TOML/INI) without users editing code directly.
- [ ] **Lifecycle Hooks**: Event hooks for `on_load`, `on_ready`, `on_shutdown`, etc.
- [ ] **Hot Reloading**: Reload mods without restarting the target application.

### Stability & Safety

- [ ] **Error Isolation**: Prevent a single crashing mod from bringing down the entire application (Safe Mode).
- [ ] **Version Compatibility**: Check if a mod is compatible with the current version of the target application or loader.
