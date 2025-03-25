import random
import time

# Character class represents both player and monsters
class Character:
    def __init__(self, name, attack, health, mana, defense):
        self.name = name
        self.attack = attack
        self.health = health
        self.mana = mana
        self.defense = defense

    def __str__(self):
        return f"{self.name}: Attack={self.attack}, Health={self.health}, Mana={self.mana}, Defense={self.defense}"

    def equip_armor(self, defense_boost):
        """Equips armor, increasing defense."""
        self.defense += defense_boost
        print(f"{self.name} equipped armor! Defense increased to {self.defense:.2f}.")

    def check_chest(self):
        """Checks a chest for armor."""
        if random.random() < 0.45:  # 45% chance of finding armor
            defense_boost = random.randint(10, 50)  # Random defense boost
            self.equip_armor(defense_boost)
        else:
            print(f"{self.name} found nothing in the chest.")

    def attack(self, target, damage):
        """Attacks another character."""
        actual_damage = damage
        self.target = target
        self.target = Monster

        if self.defense == 0:  # Damage boost if no armor
            actual_damage *= 1.03

        if target.defense > 0:
            actual_damage = max(0, actual_damage - (actual_damage * (target.defense / 100)))  # Apply damage reduction.
            target.defense = max(0, target.defense - 5)  # Reduce defense
            print(f"{self.name} attacks {target.name} for {actual_damage:.2f} damage (Defense reduced).")
        else:
            print(f"{self.name} attacks {target.name} for {actual_damage:.2f} damage (No defense).")

        target.health -= actual_damage
        target.health = max(0, target.health)  # Ensure health doesn't go below 0
        print(f"{target.name}'s health: {target.health:.2f}")

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.health -= actual_damage
        if self.health < 0:
            self.health = 0
        return actual_damage

    def is_alive(self):
        return self.health > 0

    def attack_enemy(self, enemy):
        damage = random.randint(1, self.attack)
        actual_damage = enemy.take_damage(damage)
        return actual_damage


class Swordsman(Character):
    def __init__(self, name):
        # Swordsman has higher attack, lower health, and no mana
        super().__init__(name, attack=20, health=80, mana=0, defense=100)


class Mage(Character):
    def __init__(self, name):
        # Mage has lower attack, higher health, and starting mana of 5
        super().__init__(name, attack=14, health=80, mana=15, defense=60)
        self.initial_mana = 5  # Track the starting mana


class CelestialMonk(Character):
    def __init__(self, name):
        super().__init__(name, attack=25, mana=50, defense=50, health=100)


class FrostRevenant(Character):
    def __init__(self, name):
        super().__init__(name, attack=18, mana=40, health=120, defense=50)


# The Monster class should have attack_player method already defined
class Monster(Character):
    def __init__(self, name, health, attack, defense):
        super().__init__(name, attack, health, 0, defense)
        self.name = name  # Ensure that name is assigned correctly


    def attack_player(self, player):
        damage = random.randint(1, self.attack)
        actual_damage = player.take_damage(damage)
        return actual_damage


# Modify the following monster classes to inherit from Monster, not Character
class Goblin(Monster):
    def __init__(self, name, health, attack, defense):
        super().__init__(name, health, attack, defense)

class Kobalt(Monster):
    def __init__(self, name, health, attack, defense):
        super().__init__(name, health, attack, defense)

class Skeleton(Monster):
    def __init__(self, name, health, attack, defense):
        super().__init__(name, health, attack, defense)

# Areas
class Area:
    def __init__(self, name: str, spawn_pool: list, spawn_rate: list, current_monsters: int, max_monsters: int):
        self.name = name
        self.spawn_pool = spawn_pool
        self.spawn_rate = spawn_rate
        self.current_monsters = max_monsters
        self.max_monsters = max_monsters


def defeat_monster(self):
    # Each time a monster is defeated, increase mana by 5
    self.mana += 5


def __str__(self):
    return f"{self.name}: Attack={self.attack}, Health={self.health}, Mana={self.mana}"


def choose_character():
    print("Welcome to the Tomb of the dead!,"
    "Enter at your own peril ")
    print("Choose your character class:")
    print("1. Swordsman (Higher attack, lower health, no mana)")
    print("2. Mage (Lower attack, higher health, starting mana of 5 that increases with each monster defeated)")
    print("3. FrostRevenant ( A backer, highest health and most versatile attacks with their own defense system)")
    print("4. CelestialMonk (a heavy hitter, highest starting attack power, with the ability to use mana)")

    choice = input("Enter the number of your choice (1 thru 4 ): ")

    if choice == "1":
        name = input("Enter the name of your Swordsman: ")
        character = Swordsman(name)
        print(f"\nYou have chosen {character.name}, the Swordsman!")
        print(character)
    elif choice == "2":
        name = input("Enter the name of your Mage: ")
        character = Mage(name)
        print(f"\nYou have chosen {character.name}, the Mage!")
        print(character)
    elif choice == "3":
        name = input("Enter the name of your FrostRevenant: ")
        character = FrostRevenant(name)
        print(f"\nYou have chosen {character.name}, the FrostRevenant!")
        print(character)
    elif choice == "4":
        name = input("Enter the name of your CelestialMonk: ")
        character = CelestialMonk(name)
        print(f"\nYou have chosen {character.name}, the CelestialMonk!")
        print(character)
    else:
        print("Invalid choice. Please choose either 1 or 2.")
        return choose_character()  # Restart the choice prompt if invalid input is given

    return character


# Starting the game and choosing a character
chosen_character = choose_character()

# Creating Areas
land_of_the_dead = Area("The Land of the Dead", [Goblin, Kobalt, Skeleton], [80, 10, 10], 5, 5)
frost_zone = Area("The Frost Zone", [Goblin, Kobalt, Skeleton], [50, 25, 25], 8, 8)
bottom_floor = Area("The Bottom Floor", [Goblin, Kobalt, Skeleton], [0, 40, 60], 10, 10)
# Global Variables
stage = 1


# Event-based random dungeon generation
def generate_dungeon_stage():
    # Random dungeon stage factor (can affect difficulty)
    print(f"Stage Value: {stage}")
    if stage == 1:
        return land_of_the_dead
    elif stage == 2:
        return frost_zone
    else:
        return bottom_floor


# Printing status of the game
def print_status(player, monsters):
    print(f"\n{player.name} - Health: {player.health}, Attack: {player.attack}, Defense: {player.defense}")
    for monster in monsters:
        print(f"{monster.name} - Health: {monster.health}, Attack: {monster.attack}, Defense: {monster.defense}")
    print("\n")


# Modify combat to print the actual monster names
# Modify combat to handle non-integer input gracefully
def combat(player, monsters):
    # Start combat
    while player.is_alive() and any(monster.is_alive() for monster in monsters):
        print_status(player, monsters)

        # Player's turn to attack
        print(f"{player.name}'s turn!")
        
        # Adding try-except block to handle non-integer input
        try:
            target_idx = int(input("Choose a monster to attack (1 for first, 2 for second, etc.): ")) - 1
            if target_idx >= 0 and target_idx < len(monsters) and monsters[target_idx].is_alive():
                damage = player.attack_enemy(monsters[target_idx])
                print(f"{player.name} attacks {monsters[target_idx].name} for {damage} damage!")
            else:
                print("Invalid target! No attack made.")
        except ValueError:
            # If input is not a valid integer, print "Input Invade" and continue
            print("Input Invade! Please enter a valid number.")
        
        # Monsters' turn to attack
        if any(monster.is_alive() for monster in monsters):
            time.sleep(1)  # Dramatic pause
            print("\nThe monsters are attacking!")
            for monster in monsters:
                if monster.is_alive():
                    damage = monster.attack_player(player)
                    print(f"{monster.name} attacks you for {damage} damage!")
                    
        # Check if player is still alive
        if not player.is_alive():
            print(f"\nGame Over! {player.name} has fallen in battle.")
            return False

    if not any(monster.is_alive() for monster in monsters):
        print("\nYou have defeated all the monsters!")
        return True

# Random event in the dungeon (treasure, trap, etc.)
def random_event(player):
    event = random.choice(["treasure", "trap", "nothing"])
    if event == "treasure":
        treasure_value = random.randint(1, 5)
        print(f"\nYou find a treasure chest! You gain {treasure_value} health and attack boost.")
        player.health += treasure_value
        player.attack += treasure_value
    elif event == "trap":
        trap_damage = random.randint(5, 15)
        print(f"\nYou triggered a trap! You take {trap_damage} damage.")
        player.take_damage(trap_damage)
    else:
        print("\nYou walk through the dungeon without encountering anything.")


# Modify the getMonster function to correctly instantiate the monster class
# Corrected getMonster function
# Corrected getMonster function
def getMonster(area):
    monster_ranges = []
    for i in range(len(area.spawn_rate)):
        if i == 0:
            monster_ranges.append(area.spawn_rate[i])
        else:
            monster_ranges.append(area.spawn_rate[i] + monster_ranges[i - 1])
    
    dice_roll = random.randint(0, 100)
    for i in range(len(monster_ranges)):
        if monster_ranges[i] > dice_roll:
            # Get the monster class from the spawn pool
            monster_class = area.spawn_pool[i]
            return monster_class  # Return the class itself (e.g., Goblin, Kobalt)



# Game loop
def start_game():
    # Initial random stage setup
    area = generate_dungeon_stage()
    print(f"\nYou are about to enter the {area.name}. Prepare yourself!")

    # Prepare monsters for this dungeon
    monster_count = random.randint(1, area.current_monsters)
    area.current_monsters -= monster_count
    if area.current_monsters == 0:
        global stage
        stage += 1
    monsters = []


    # Inside start_game() function, where monsters are being created
    for i in range(monster_count):
        monster_type = getMonster(area)  # This returns a class (e.g., Goblin, Kobalt)
    
    # Make sure that we are correctly calling the class constructor to create a monster instance
        monster_name = monster_type.__name__  # This gives the class name (Goblin, Kobalt, skeleton)
        monster_health = random.randint(10, 50)  # Example health stat
        monster_attack = random.randint(5, 20)  # Example attack stat
        monster_defense = random.randint(2, 5)  # Example defense stat
    
    # Instantiate the monster class correctly and append it
        monsters.append(monster_type(monster_name, monster_health, monster_attack, monster_defense))




    # Game loop
    dungeon_level = 1
    while chosen_character.is_alive():
        print(f"\n--- Dungeon Level {dungeon_level} ---")
        random_event(chosen_character)
        if not combat(chosen_character, monsters):
            break

        # Proceed to next dungeon level
        dungeon_level += 1
        monsters = []  # Reset monsters after level

        if dungeon_level < 7:
            # Re-generate new monsters for next level
            monster_count = random.randint(3, 6)
            for i in range(monster_count):
                monster_name = f"Monster-{i+1}"
                monster_attack = random.randint(1, 10)
                monster_health = random.randint(15, 30)
                monster_defense = random.randint(2, 5)
                # Use getMonster to decide which type of monster will be spawned
                monster_type = getMonster(area)
                if monster_type:
                    monsters.append(monster_type(monster_name, monster_health, monster_attack, monster_defense))
        elif dungeon_level == 7:
            # Final Boss Battle - Dungeon Level 7
            print('You have arrived at the bottom of hell!')
            final_boss = Monster("LordOfTheTomb", 50, 100, 20)
            final_boss.mana = 100
            monsters.append(final_boss)
        else:
            end_game()
            return

    print(f"\n{chosen_character.name} has died. Game Over!")


def end_game():
    print("Game Over! Better luck next time.")
    exit()


if __name__ == "__main__":
    start_game()
