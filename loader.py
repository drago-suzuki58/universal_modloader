import argparse
import ast
import importlib.util
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODS_DIR = os.path.join(ROOT_DIR, "mods")
FRAMEWORK_DIR = os.path.join(MODS_DIR, "universal_modloader")


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
    parser = argparse.ArgumentParser(description="Universal Mod Loader")
    parser.add_argument(
        "target_script",
        nargs="?",
        default="main.py",
        help="The Python script to launch with mods (default: main.py)",
    )

    args, game_args = parser.parse_known_args()

    target_script = args.target_script

    target_module_name = os.path.splitext(os.path.basename(target_script))[0]

    print("--- Universal Mod Loader (UML) ---\n")
    print(f"[Loader] Target: {target_script} ({target_module_name})")

    uml_init = os.path.join(FRAMEWORK_DIR, "__init__.py")
    if not os.path.exists(uml_init):
        print(f"[Critical] Framework not found at: {FRAMEWORK_DIR}")
        return

    print("[Loader] Loading Framework...")
    uml = load_module_from_path("universal_modloader", uml_init)

    if not uml:
        print("[Critical] Failed to load framework.")
        return

    from universal_modloader import install  # type: ignore

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

    if not os.path.exists(target_script):
        print(f"[Error] Target script '{target_script}' not found.")
        return

    print(f"[Loader] Launching {target_script} with Injection...\n")

    with open(target_script, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = ast.parse(source_code, filename=target_script)

    from universal_modloader.core.transformer import MainTransformer  # type: ignore

    transformer = MainTransformer(target_module_name)

    tree = transformer.visit(tree)
    ast.fix_missing_locations(tree)

    sys.argv = [target_script] + game_args

    global_context = {
        "__name__": "__main__",
        "__file__": target_script,
        "__doc__": None,
    }

    try:
        code_obj = compile(tree, filename=target_script, mode="exec")
        exec(code_obj, global_context)

    except KeyboardInterrupt:
        print("\n[Loader] Terminated.")
    except Exception as e:
        print(f"\n[Loader] Game Crashed: {e}")


if __name__ == "__main__":
    main()
