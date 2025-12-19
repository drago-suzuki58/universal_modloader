@echo off

set ROOT_DIR=%~dp0

if exist "%ROOT_DIR%loader.py" (
    copy "%ROOT_DIR%loader.py" "%ROOT_DIR%examples\simple_cli_rpg\loader.py"
    copy "%ROOT_DIR%loader.py" "%ROOT_DIR%examples\time_debugging\loader.py"
    copy "%ROOT_DIR%loader.py" "%ROOT_DIR%examples\modded_print\loader.py"

    REM Other example projects can be added here in the future
) else (
    echo Error: loader.py not found in %ROOT_DIR%
    exit /b 1
)

if exist "%ROOT_DIR%mods\universal_modloader" (
    xcopy "%ROOT_DIR%mods\universal_modloader" "%ROOT_DIR%examples\simple_cli_rpg\mods\universal_modloader" /E /I /Y
    xcopy "%ROOT_DIR%mods\universal_modloader" "%ROOT_DIR%examples\time_debugging\mods\universal_modloader" /E /I /Y
    xcopy "%ROOT_DIR%mods\universal_modloader" "%ROOT_DIR%examples\modded_print\mods\universal_modloader" /E /I /Y

    REM Other example projects can be added here in the future
) else (
    echo Error: mods\universal_modloader not found in %ROOT_DIR%
    exit /b 1
)
