# pandas_hack

[日本語](./README.ja.md) | English

This example demonstrates how to inject observability tools (progress bar, timer, data inspector) into a slow data processing script without adding any new dependencies to the target project.

## The Target

A typical data processing script found in data engineering workflows.

It lacks **observability** and provides **no user feedback** during execution.

- **Stack:** Pandas, NumPy, Time (Standard Library).
- **Behavior:**
  - Simulates heavy computation using `time.sleep` inside a `df.apply` loop.
  - Runs silently for several seconds, leaving the user unsure if the process has frozen.
  - Provides no progress indicators or performance metrics.

## The Mod

The Mod injects observability tools directly into the runtime, without adding dependencies　to the project.

- **Native Progress Bar (progress_bar.py):**
  - Wraps the function passed to `df.apply` using a Higher-Order Function approach.
  - Renders a real-time CLI progress bar using only `sys.stdout` and standard libraries.
- **Execution Timer (check_execution_time.py):**
  - Hooks into the `HEAD` and `TAIL` of the processing function.
  - Measures and prints the precise execution time to help identify bottlenecks.
- **Result Inspector (check_result.py):**
  - Accesses the local variable scope (`locals()`) at the end of the process.
  - Peeks at the result DataFrame and prints a preview to verify data integrity.

## How to Run

### Prerequisite

Ensure you have `uv` installed and dependencies synced.

### 1. Run Modded (With UML)

The magic happens here. The loader injects the mod into the target.

```bash
cd examples/pandas_hack
# Run the target via the Universal Modloader
uv run loader.py
```

**Try this:**  
Watch the console. A progress bar will appear and update in real-time, followed by the execution time and a data preview, turning a silent script into an observable one.

### 2. Run Vanilla (Original)

Verify the original behavior (secure/boring/slow).

```bash
cd examples/pandas_hack
uv run main.py
```

**Try this:**  
Notice that the script "hangs" silently while processing and only prints messages at the very beginning and end.
