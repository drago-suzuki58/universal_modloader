#!/bin/bash

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$ROOT_DIR/loader.py" ]; then
    cp "$ROOT_DIR/loader.py" "$ROOT_DIR/examples/simple_cli_rpg/loader.py"
    
    # Other example projects can be added here in the future
else
    echo "Error: loader.py not found in $ROOT_DIR"
    exit 1
fi

if [ -d "$ROOT_DIR/mods/universal_modloader" ]; then
    cp -r "$ROOT_DIR/mods/universal_modloader" "$ROOT_DIR/examples/simple_cli_rpg/mods/universal_modloader"
    
    # Other example projects can be added here in the future
else
    echo "Error: mods/universal_modloader not found in $ROOT_DIR"
    exit 1
fi
