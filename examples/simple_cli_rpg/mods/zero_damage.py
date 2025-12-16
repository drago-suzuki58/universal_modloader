import universal_modloader as uml


@uml.Inject("main", "Player.take_damage", at=uml.At.HEAD())
def on_calculate_damage(ctx):
    ctx["amount"] = 0
    print("[Mod] System: Damage nullified!")
