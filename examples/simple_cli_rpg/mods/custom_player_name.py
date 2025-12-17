import universal_modloader as uml

CUSTOM_PLAYER_NAME = "ModdedHero"

@uml.Inject("main", "main", at=uml.At.INVOKE("Player"))
def customize_name(ctx):
    original_name = ctx['args'][0]
    ctx['args'][0] = CUSTOM_PLAYER_NAME
    print(f"[Mod] Player name changed from '{original_name}' to '{CUSTOM_PLAYER_NAME}'")
