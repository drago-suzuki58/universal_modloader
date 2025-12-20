import time

import universal_modloader as uml


@uml.Inject("main", "process_data", at=uml.At.HEAD())
@uml.Inject("main", "process_data", at=uml.At.TAIL())
def start_stop_timer(ctx):
    if ctx.get("start_time") is not None:
        elapsed_time = time.time() - ctx["start_time"]
        print(f"[Mod] Elapsed Time: {elapsed_time:.2f} seconds.")
        ctx["start_time"] = None
    else:
        ctx["start_time"] = time.time()
        print("[Mod] Timer started.")
