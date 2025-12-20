# simple_cli_rpg

[日本語](./README.ja.md) | English

This example demonstrates how to manipulate game logic, implementing common cheat features like "God Mode" and "Speedhacks" by hooking into the game loop and state management.

## The Target

A simple Command Line Interface (CLI) Role-Playing Game.

It is designed with **intentional friction** and hardcoded parameters.

- **Stack:** Python Standard Library (random, time).
- **Behavior:**
  - **Slow Gameplay:** Enforces a mandatory 1-second delay (`time.sleep`) after every action (exploration, combat), making the game sluggish.
  - **Standard Difficulty:** The player takes damage from enemies during the combat phase.
  - **Fixed Identity:** The player name is hardcoded (e.g., "Hero") and cannot be changed via arguments.

## The Mod

The Mods modify the game rules and internal state to remove friction and trivialize the difficulty.

- **Custom Player Name (custom_player_name.py):**
  - Overwrites the player's name attribute at runtime.
  - Demonstrates dynamic state injection into existing objects.
- **Speedhack / No Sleep (no_sleep_time.py):**
  - Hooks into the delay function.
  - Completely bypasses the artificial 1-second cooldown, making the gameplay instant and responsive.
- **God Mode / Zero Damage (zero_damage.py):**
  - Hooks into the combat damage calculation logic.
  - Forces all incoming damage from enemies to be `0`, rendering the player invincible.

## How to Run

### Prerequisite

Ensure you have `uv` installed and dependencies synced.

### 1. Run Modded (Cheated)

The loader injects the cheats into the game.

```bash
cd examples/simple_cli_rpg
# Run the target via the Universal Modloader
uv run loader.py
```

**Try this:**  
Play the game. Notice that there is no delay between actions, your name is customized, and you take no damage in battles.

### 2. Run Vanilla (Original)

Verify the original slow and difficult behavior.

```bash
cd examples/simple_cli_rpg
uv run main.py
```

**Try this:**  
Experience the frustrating 1-second delay after every input and verify that you lose health when attacked.
