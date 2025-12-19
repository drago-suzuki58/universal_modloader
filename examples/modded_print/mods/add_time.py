import datetime

import universal_modloader as uml


@uml.Inject("main", at=uml.At.INVOKE("print"))
def add_time(ctx):
    original_message = ctx["args"][0]
    modified_message = f"{datetime.datetime.now()}: {original_message}"
    ctx["args"][0] = modified_message
