import random
import sys
import time


class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.potions = 3

    def attack(self):
        damage = self.calculate_damage()
        print(f"You attacked! Dealt {damage} damage.")
        return damage

    def calculate_damage(self):
        base = random.randint(5, 15)
        return base

    def heal(self):
        if self.potions > 0:
            self.potions -= 1
            heal_amount = 30
            self.hp = min(self.hp + heal_amount, self.max_hp)
            print(
                f"You used a potion. HP recovered to {self.hp}. (Potions left: {self.potions})"
            )
        else:
            print("No potions left!")

    def take_damage(self, amount):
        self.hp -= amount
        print(f"Ouch! You took {amount} damage. Current HP: {self.hp}")
        if self.hp <= 0:
            print("--- YOU DIED ---")
            print("Thank you for playing!")
            sys.exit()


class Enemy:
    def __init__(self, name, hp, damage_max):
        self.name = name
        self.hp = hp
        self.damage_max = damage_max

    def is_alive(self):
        return self.hp > 0


def print_intro():
    print("\n" + "=" * 40)
    print(" Welcome to the Simple CLI RPG!")
    print(" Defeat the Demon King to save the world.")
    print("=" * 40 + "\n")
    time.sleep(1)


def explore_event(player):
    print("\nYou walk through the dark corridor...")
    time.sleep(1)

    encounter = random.randint(1, 3)
    if encounter == 1:
        print("You found a treasure chest! (Potions +1)")
        player.potions += 1
    else:
        enemy_type = random.choice(["Goblin", "Skeleton", "Orc"])
        enemy = Enemy(enemy_type, hp=30, damage_max=10)
        print(f"A wild {enemy.name} appeared!")
        battle_loop(player, enemy)


def battle_loop(player, enemy):
    while enemy.is_alive():
        print(f"\n[Enemy: {enemy.name} (HP: {enemy.hp})]")
        print(f"[Player: {player.name} (HP: {player.hp}) | Potions: {player.potions}]")
        print("1. Attack")
        print("2. Heal")
        print("3. Run")

        choice = input("Select action (1-3): ")
        print()

        if choice == "1":
            dmg = player.attack()
            enemy.hp -= dmg
        elif choice == "2":
            player.heal()
        elif choice == "3":
            print("You ran away!")
            return
        else:
            print("Invalid input.")
            continue

        if enemy.is_alive():
            dmg = random.randint(1, enemy.damage_max)
            print(f"{enemy.name} attacks you!")
            player.take_damage(dmg)
        time.sleep(1)

    print(f"You defeated {enemy.name}!")


def main():
    print_intro()
    player = Player("Hero")

    while True:
        print("\n--- Main Menu ---")
        print("1. Explore Dungeon")
        print("2. Rest (Restore HP)")
        print("3. Quit Game")

        choice = input("Select (1-3): ")

        if choice == "1":
            explore_event(player)
        elif choice == "2":
            print("You rested at the campfire.")
            player.hp = player.max_hp
            print("HP fully recovered!")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid input.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame exited.")
