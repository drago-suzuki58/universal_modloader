import universal_modloader as uml


@uml.Inject("main", at=uml.At.INVOKE("print"))
def rgb_console(ctx):
    if not ctx["args"]:
        return

    color_patterns = [
        "\033[91m",
        "\033[93m",
        "\033[92m",
        "\033[96m",
        "\033[94m",
        "\033[95m",
    ]

    original_message = " ".join(map(str, ctx["args"]))
    new_message = ""

    for i, char in enumerate(original_message):
        color_code = color_patterns[i % len(color_patterns)]
        new_message += f"{color_code}{char}\033[0m"

    ctx["args"][:] = [new_message]
