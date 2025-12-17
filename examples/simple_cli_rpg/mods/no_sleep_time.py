import universal_modloader as uml

@uml.Inject("main", at=uml.At.INVOKE("time.sleep"))
def prevent_sleep(ctx):
    ctx["__cancel__"] = True
    print("[Mod] System: Sleep function call prevented!")
