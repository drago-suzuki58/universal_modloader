from datetime import datetime

import universal_modloader as uml


@uml.Inject(
    "main",
    "SubscriptionManager.__init__",
    at=uml.At.INVOKE("datetime.now", shift=uml.Shift.AFTER),
)
def on_init_time(ctx):
    print("[Mod] System: Setting subscription start time to leap day.")
    ctx["__return__"] = datetime(2024, 2, 29, 12, 0, 0)
