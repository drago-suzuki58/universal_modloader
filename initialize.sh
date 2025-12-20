#!/bin/bash

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$ROOT_DIR/loader.py" ]; then
    cp "$ROOT_DIR/loader.py" "$ROOT_DIR/examples/simple_cli_rpg/loader.py"
    cp "$ROOT_DIR/loader.py" "$ROOT_DIR/examples/time_debugging/loader.py"
    cp "$ROOT_DIR/loader.py" "$ROOT_DIR/examples/modded_print/loader.py"
    cp "$ROOT_DIR/loader.py" "$ROOT_DIR/examples/fastapi_evil_security/loader.py"
    cp "$ROOT_DIR/loader.py" "$ROOT_DIR/examples/tkinter_pytools/loader.py"
    cp "$ROOT_DIR/loader.py" "$ROOT_DIR/examples/pandas_hack/loader.py"

    # Other example projects can be added here in the future
else
    echo "Error: loader.py not found in $ROOT_DIR"
    exit 1
fi

if [ -d "$ROOT_DIR/mods/universal_modloader" ]; then
    cp -r "$ROOT_DIR/mods/universal_modloader" "$ROOT_DIR/examples/simple_cli_rpg/mods/universal_modloader"
    cp -r "$ROOT_DIR/mods/universal_modloader" "$ROOT_DIR/examples/time_debugging/mods/universal_modloader"
    cp -r "$ROOT_DIR/mods/universal_modloader" "$ROOT_DIR/examples/modded_print/mods/universal_modloader"
    cp -r "$ROOT_DIR/mods/universal_modloader" "$ROOT_DIR/examples/fastapi_evil_security/mods/universal_modloader"
    cp -r "$ROOT_DIR/mods/universal_modloader" "$ROOT_DIR/examples/tkinter_pytools/mods/universal_modloader"
    cp -r "$ROOT_DIR/mods/universal_modloader" "$ROOT_DIR/examples/pandas_hack/mods/universal_modloader"

    # Other example projects can be added here in the future
else
    echo "Error: mods/universal_modloader not found in $ROOT_DIR"
    exit 1
fi
