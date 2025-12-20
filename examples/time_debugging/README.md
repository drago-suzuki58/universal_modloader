# time_debugging

[日本語](./README.ja.md) | English

This example demonstrates **Time-Travel Debugging**. It shows how to mock system time at runtime to test edge cases (like leap years) in time-sensitive logic, such as subscription management, without changing the OS clock.

## The Target

A simple Subscription Manager class.

It calculates expiration dates and checks validity based on the "current" time.

- **Stack:** Python Standard Library (`datetime`).
- **Behavior:**
  - Uses `datetime.datetime.now()` to determine the current date.
  - Logic may behave differently or fail depending on the specific date (e.g., handling February 29th in a leap year).
  - Testing specific dates usually requires waiting or changing the system time.

## The Mod

The Mod mocks the time source to force the application to believe it is currently a leap year.

- **Leap Year Injection (leap_year.py):**
  - Hooks into `datetime.now()` (or the specific time retrieval method used by the target).
  - Overrides the return value to a fixed date in a leap year (e.g., February 29th, 2024).
  - Allows instant verification of logic that handles leap year calculations.

## How to Run

### Prerequisite

Ensure you have `uv` installed and dependencies synced.

### 1. Run Modded (Time Travel)

The loader runs the script with the mocked time.

```bash
cd examples/time_debugging
# Run the target via the Universal Modloader
uv run loader.py
```

**Try this:**  
Observe the output date. It will be fixed to the specific leap year date defined in the Mod, regardless of the actual real-world time.

### 2. Run Vanilla (Real Time)

Runs the script using the actual system time.

```bash
cd examples/time_debugging
uv run main.py
```

**Try this:**  
Confirm that the output reflects the current actual date and time.
