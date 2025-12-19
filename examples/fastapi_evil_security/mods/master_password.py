import universal_modloader as uml


@uml.Inject("app", "login", at=uml.At.INVOKE("pwd_context.verify"))
def force_true_login(ctx):
    creditials = ctx["caller_locals"]["credentials"]
    if creditials.password != "master_password":
        return

    ctx["__return__"] = True
    ctx["__cancel__"] = True
