import universal_modloader as uml


@uml.Inject("main", at=uml.At.INVOKE("print"))
def add_time(ctx):
    original_message = ctx["args"][0]
    ctx["args"][0] = f"{original_message} :)"
