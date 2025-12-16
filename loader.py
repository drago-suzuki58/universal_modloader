import ast
import importlib.util
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODS_DIR = os.path.join(ROOT_DIR, "mods")
FRAMEWORK_DIR = os.path.join(MODS_DIR, "universal_modloader")
TARGET_SCRIPT = "main.py"


def load_module_from_path(module_name, file_path):
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            print(f"  [Error] Could not create spec for: {file_path}")
            return None

        module = importlib.util.module_from_spec(spec)

        sys.modules[module_name] = module

        spec.loader.exec_module(module)

        return module
    except Exception as e:
        print(f"  [Error] Failed to load {module_name}: {e}")
        return None


def main():
    print("--- Universal Mod Loader (Safe Mode) ---\n")

    uml_init = os.path.join(FRAMEWORK_DIR, "__init__.py")
    if not os.path.exists(uml_init):
        print(f"[Critical] Framework not found at: {FRAMEWORK_DIR}")
        return

    print("[Loader] Loading Framework...")
    uml = load_module_from_path("universal_modloader", uml_init)

    if not uml:
        print("[Critical] Failed to load framework.")
        return

    from universal_modloader.install import install  # type: ignore

    install()
    print("  -> Framework installed.\n")

    print("[Loader] Loading Mods...")
    if not os.path.exists(MODS_DIR):
        os.makedirs(MODS_DIR)

    count = 0
    for item in sorted(os.listdir(MODS_DIR)):
        item_path = os.path.join(MODS_DIR, item)

        if item == "universal_modloader" or item.startswith("__"):
            continue

        mod_name = None
        entry_point = None

        if os.path.isdir(item_path):
            init_file = os.path.join(item_path, "__init__.py")
            if os.path.exists(init_file):
                mod_name = item
                entry_point = init_file

        elif os.path.isfile(item_path) and item.endswith(".py"):
            mod_name = item[:-3]
            entry_point = item_path

        if mod_name and entry_point:
            print(f"  + Loading: {mod_name} ...")
            load_module_from_path(mod_name, entry_point)
            count += 1

    print(f"\n[Loader] {count} mods loaded.")
    print("-" * 40)

    if not os.path.exists(TARGET_SCRIPT):
        print(f"[Error] {TARGET_SCRIPT} not found.")
        return

    print(f"[Loader] Launching {TARGET_SCRIPT} with Injection...\n")

    with open(TARGET_SCRIPT, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = ast.parse(source_code, filename=TARGET_SCRIPT)

    from universal_modloader.core import InjectionTransformer  # type: ignore

    transformer = InjectionTransformer("main")

    tree = transformer.visit(tree)
    ast.fix_missing_locations(tree)

    sys.argv = [TARGET_SCRIPT] + sys.argv[1:]

    global_context = {
        "__name__": "__main__",
        "__file__": TARGET_SCRIPT,
        "__doc__": None,
    }

    try:
        code_obj = compile(tree, filename=TARGET_SCRIPT, mode="exec")

        exec(code_obj, global_context)

    except KeyboardInterrupt:
        print("\n[Loader] Terminated.")
    except Exception as e:
        print(f"\n[Loader] Game Crashed: {e}")


if __name__ == "__main__":
    main()
