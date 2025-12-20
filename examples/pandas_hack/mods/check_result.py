import universal_modloader as uml


@uml.Inject("main", "process_data", at=uml.At.TAIL())
def peek_result(ctx):
    if "df" in ctx:
        print("\n[Mod] Checking final data...")
        print(ctx["df"].head(3))
