import sys
import time

import universal_modloader as uml


@uml.Inject(
    "main", "process_data", at=uml.At.INVOKE("df.apply", shift=uml.Shift.BEFORE)
)
def inject_native_progress(ctx):
    df = ctx["caller_locals"]["df"]
    total_rows = len(df)

    original_func = ctx["args"][0]

    state = {"count": 0, "start_time": time.time()}

    def wrapper_func(row):
        state["count"] += 1
        current = state["count"]

        percent = (current / total_rows) * 100

        bar_length = 30
        filled_length = int(bar_length * current // total_rows)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)

        elapsed = time.time() - state["start_time"]

        sys.stdout.write(
            f"\r[Mod] Progress: [{bar}] {percent:.1f}% ({current}/{total_rows}) {elapsed:.2f}s"
        )
        sys.stdout.flush()

        if current == total_rows:
            sys.stdout.write("\n")

        return original_func(row)

    print("[Mod] Injecting native progress bar wrapper...")
    ctx["args"][0] = wrapper_func
