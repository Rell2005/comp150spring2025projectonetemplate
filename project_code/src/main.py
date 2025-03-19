import random
import time
import json
from typing import List, Optional
from enum import Enum


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Statistic:
    def __init__(self, name: str, value: int = 0, description: str = "", min_value: int = 0, max_value: int = 100):
        self.name = name
        self.value = value
        self.description = description
        self.min_value = min_value
        self.max_value = max_value

    def __str__(self):
        return f"{self.name}: {self.value}"

    def modify(self, amount: int):
        self.value = max(self.min_value, min(self.max_value, self.value + amount))


# Base Character class that combines aspects from both files
class Character:
    def __init__(self, name: str, attack: int = 10, health: int = 50, mana: int = 0, defense: int = 10):
        self.name = name
        # Basic combat stats
        self.attack = attack
        self.health = health
        self.mana = mana
        self.defense = defense

        # Advanced character stats
        self.strength = Statistic("Strength", attack, "Strength is a measure of physical power.")
        self.intelligence = Statistic("Intelligence", mana, "Intelligence is a measure of cognitive ability.")
        self.constitution = Statistic("Constitution", health // 5, "Constitution affects health and resistance.")

    def __str__(self):
        return f"{self.name}: Attack={self.attack}, Health={self.health}, Mana={self.mana}, Defense={self.defense}"

    def get_stats(self):
        return [self.strength, self.intelligence, self.constitution]

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

    def take_damage(self, damage):
        """Takes damage, reduced by defense."""
        actual_damage = max(0, damage - (damage * (self.defense / 100)))
        self.health -= actual_damage
        if self.health < 0:
            self.health = 0
        return actual_damage

    def is_alive(self):
        """Checks if the character is still alive."""
        return self.health > 0

    def attack_enemy(self, enemy):
        """Attacks an enemy, dealing damage based on attack stat."""
        damage = random.randint(1, self.attack)

        # Apply damage modifiers based on class types
        actual_damage = damage

        # Apply defense reduction
        if enemy.defense > 0:
            actual_damage = max(0, actual_damage - (actual_damage * (enemy.defense / 100)))
            enemy.defense = max(0, enemy.defense - 5)  # Reduce defense
            print(f"{self.name} attacks {enemy.name} for {actual_damage:.2f} damage (Defense reduced).")
        else:
            print(f"{self.name} attacks {enemy.name} for {actual_damage:.2f} damage (No defense).")

        # Apply damage
        enemy.health -= actual_damage
        enemy.health = max(0, enemy.health)  # Ensure health doesn't go below 0

        print(f"{enemy.name}'s health: {enemy.health:.2f}")
        return actual_damage


class Swordsman(Character):
    def __init__(self, name):
        # Swordsman has higher attack, lower health, and no mana
        super().__init__(name, attack=20, health=50, mana=0, defense=10)
        self.strength.value = 20  # Higher strength for swordsman


class Mage(Character):
    def __init__(self, name):
        # Mage has lower attack, higher health, and starting mana of 5
        super().__init__(name, attack=10, health=80, mana=5, defense=5)
        self.intelligence.value = 20  # Higher intelligence for mage
        self.initial_mana = 5  # Track the starting mana

    def defeat_monster(self):
        # Each time a monster is defeated, increase mana by 5
        self.mana += 5
        self.intelligence.modify(1)  # Intelligence also increases slightly


class Monster(Character):
    def __init__(self, name, health, attack, defense):
        super().__init__(name, attack=attack, health=health, mana=0, defense=defense)

    def attack_player(self, player):
        """Monster attacks a player character."""
        return self.attack_enemy(player)


class Event:
    def __init__(self, data: dict):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.prompt_text = data['prompt_text']
        self.pass_message = data['pass']['message']
        self.fail_message = data['fail']['message']
        self.partial_pass_message = data['partial_pass']['message']
        self.status = EventStatus.UNKNOWN

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)

    def resolve_choice(self, character: Character, chosen_stat: Statistic):
        if chosen_stat.name == self.primary_attribute:
            self.status = EventStatus.PASS
            print(self.pass_message)
            # Reward for passing
            character.strength.modify(2)
            character.health += 10
        elif chosen_stat.name == self.secondary_attribute:
            self.status = EventStatus.PARTIAL_PASS
            print(self.partial_pass_message)
            # Small reward for partial pass
            character.health += 5
        else:
            self.status = EventStatus.FAIL
            print(self.fail_message)
            # Penalty for failing
            character.take_damage(5)


class Location:
    def __init__(self, name: str, events: List[Event] = None, monsters: List[Monster] = None):
        self.name = name
        self.events = events or []
        self.monsters = monsters or []

    def get_event(self) -> Event:
        if self.events:
            return random.choice(self.events)
        return None

    def generate_monsters(self, min_attack, max_attack, min_health, count=None):
        """Generate a random number of monsters for this location."""
        if count is None:
            count = random.randint(3, 6)

        self.monsters = []
        for i in range(count):
            monster_name = f"Monster-{i+1}"
            monster_attack = random.randint(min_attack, max_attack)
            monster_health = random.randint(min_health, min_health + 10)
            monster_defense = random.randint(2, 5)
            self.monsters.append(Monster(monster_name, monster_health, monster_attack, monster_defense))

        return self.monsters


class UserInputParser:
    def parse(self, prompt: str) -> str:
        return input(prompt)

    def select_party_member(self, party: List[Character]) -> Character:
        print("Choose a party member:")
        for idx, member in enumerate(party):
            print(f"{idx + 1}. {member.name}")
        choice = int(self.parse("Enter the number of the chosen party member: ")) - 1
        return party[choice]

    def select_stat(self, character: Character) -> Statistic:
        print(f"Choose a stat for {character.name}:")
        stats = character.get_stats()
        for idx, stat in enumerate(stats):
            print(f"{idx + 1}. {stat.name} ({stat.value})")
        choice = int(self.parse("Enter the number of the stat to use: ")) - 1
        return stats[choice]


def load_events_from_json(file_path: str) -> List[Event]:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return [Event(event_data) for event_data in data]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading events: {e}")
        # Return some default events if file can't be loaded
        return [
            Event({
                'primary_attribute': 'Strength',
                'secondary_attribute': 'Constitution',
                'prompt_text': 'You encounter a heavy boulder blocking your path.',
                'pass': {'message': 'With your great strength, you push the boulder aside!'},
                'fail': {'message': 'You struggle but cannot move the boulder.'},
                'partial_pass': {'message': 'You manage to roll the boulder a bit, creating a small passage.'}
            }),
            Event({
                'primary_attribute': 'Intelligence',
                'secondary_attribute': 'Strength',
                'prompt_text': 'You find an ancient puzzle lock on a treasure chest.',
                'pass': {'message': 'Your intelligence helps you solve the puzzle easily!'},
                'fail': {'message': 'The puzzle confounds you, and the chest remains locked.'},
                'partial_pass': {'message': 'You brute force some of the mechanisms and partially open the chest.'}
            })
        ]


def choose_character():
    print("Welcome to the Dungeon Adventure!")
    print("Choose your character class:")
    print("1. Swordsman (Higher attack, lower health, no mana)")
    print("2. Mage (Lower attack, higher health, starting mana of 5 that increases with each monster defeated)")

    choice = input("Enter the number of your choice (1 or 2): ")

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
    else:
        print("Invalid choice. Please choose either 1 or 2.")
        return choose_character()  # Restart the choice prompt if invalid input is given

    return character


def generate_dungeon_stage():
    # Random dungeon stage factor (can affect difficulty)
    stage_value = random.randint(1, 10)
    print(f"Stage Value: {stage_value}")

    if stage_value <= 3:
        return "Goblin Lair", 3, 5, 8  # Location name, Min Attack, Max Attack, Min Health
    elif stage_value <= 7:
        return "Cursed Tomb", 5, 10, 12
    else:
        return "Dragon's Den", 8, 15, 20


def print_status(player, monsters):
    print(f"\n{player.name} - Health: {player.health}, Attack: {player.attack}, Defense: {player.defense}")
    for monster in monsters:
        if monster.is_alive():
            print(f"{monster.name} - Health: {monster.health}, Attack: {monster.attack}, Defense: {monster.defense}")
    print("\n")


def combat(player, monsters):
    # Start combat
    while player.is_alive() and any(monster.is_alive() for monster in monsters):
        print_status(player, monsters)

        # Player's turn to attack
        print(f"{player.name}'s turn!")
        alive_monsters = [monster for monster in monsters if monster.is_alive()]
        if not alive_monsters:
            break

        for idx, monster in enumerate(alive_monsters):
            print(f"{idx + 1}. {monster.name} (Health: {monster.health})")

        target_idx = int(input("Choose a monster to attack (1 for first, 2 for second, etc.): ")) - 1
        if 0 <= target_idx < len(alive_monsters):
            player.attack_enemy(alive_monsters[target_idx])
        else:
            print("Invalid target! No attack made.")

        # Monsters' turn to attack
        if any(monster.is_alive() for monster in monsters):
            time.sleep(1)  # Dramatic pause
            print("\nThe monsters are attacking!")
            for monster in monsters:
                if monster.is_alive():
                    damage = monster.attack_player(player)
                    print(f"{monster.name} attacks you for {damage:.2f} damage!")

        # Check if player is still alive
        if not player.is_alive():
            print(f"\nGame Over! {player.name} has fallen in battle.")
            return False

    if not any(monster.is_alive() for monster in monsters):
        print("\nYou have defeated all the monsters!")
        # If player is a mage, increase mana for each monster defeated
        if isinstance(player, Mage):
            player.defeat_monster()
            print(f"{player.name} gains mana! Current mana: {player.mana}")
        return True


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
        print("\nYou walk through the dungeon without encountering anything special.")


class Game:
    def __init__(self, parser=None):
        self.parser = parser or UserInputParser()
        self.player = None
        self.party = []
        self.locations = []
        self.continue_playing = True
        self.current_location = None
        self.dungeon_level = 1

    def initialize(self):
        # Create player character
        self.player = choose_character()
        self.party = [self.player]

        # Load events
        try:
            events = load_events_from_json('location_events/location_1.json')
        except:
            events = load_events_from_json('location_1.json')

        # Create initial location
        dungeon_name, min_attack, max_attack, min_health = generate_dungeon_stage()
        self.current_location = Location(dungeon_name, events)
        self.current_location.generate_monsters(min_attack, max_attack, min_health)

        print(f"\nYou are about to enter the {dungeon_name}. Prepare yourself!")

    def start(self):
        self.initialize()

        while self.continue_playing and self.player.is_alive():
            print(f"\n--- Dungeon Level {self.dungeon_level} ---")

            # Chance for random event
            random_event(self.player)

            # Chance for special event from the event system
            if random.random() < 0.3:  # 30% chance of special event
                event = self.current_location.get_event()
                if event:
                    event.execute(self.party, self.parser)

            # Combat encounter
            if not combat(self.player, self.current_location.monsters):
                self.continue_playing = False
                break

            # Proceed to next dungeon level
            self.dungeon_level += 1

            # Generate new location and monsters
            dungeon_name, min_attack, max_attack, min_health = generate_dungeon_stage()
            self.current_location = Location(dungeon_name, self.current_location.events)
            self.current_location.generate_monsters(min_attack, max_attack, min_health)

            print(f"\nYou advance to level {self.dungeon_level}!")
            print(f"You enter the {self.current_location.name}. Prepare for battle!")

            # Ask if player wants to continue
            choice = input("\nDo you want to continue to the next level? (y/n): ").lower()
            if choice != 'y':
                print("You decide to rest and end your adventure for now.")
                self.continue_playing = False

        if not self.player.is_alive():
            print(f"\n{self.player.name} has died. Game Over!")
        else:
            print(f"\nCongratulations! {self.player.name} survived {self.dungeon_level} levels of the dungeon!")
            print(f"Final stats: {self.player}")


if __name__ == "__main__":
    game = Game()
    game.start()