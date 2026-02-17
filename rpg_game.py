#!/usr/bin/env python3
"""
Text-based RPG Game
A simple adventure game with combat, exploration, and character progression.
"""
import sys
from character import Player
from world import GameWorld
from items import create_item
from save_load import save_game, load_game, has_save_file


def display_title():
    """Display game title"""
    print("\n" + "="*50)
    print("  🗡️  TEXT RPG ADVENTURE  🗡️")
    print("="*50)


def create_character():
    """Create a new player character"""
    print("\n📝 Character Creation")
    print("-" * 50)
    
    name = input("Enter your character's name: ").strip()
    if not name:
        name = "Hero"
    
    print("\nChoose your class:")
    print("1. Warrior - High HP and Attack, Low MP")
    print("2. Mage - High MP and Magic, Low Defense")
    print("3. Rogue - Balanced stats, versatile")
    
    choice = input("\nChoice (1-3): ").strip()
    
    char_class = "Warrior"
    if choice == "2":
        char_class = "Mage"
    elif choice == "3":
        char_class = "Rogue"
    
    player = Player(name, char_class)
    
    # Give starting items
    player.add_item(create_item('health_potion'))
    player.add_item(create_item('health_potion'))
    
    print(f"\n✨ Welcome, {name} the {char_class}!")
    return player


def main_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("MAIN MENU")
    print("="*50)
    print("1. New Game")
    
    if has_save_file():
        print("2. Load Game")
        print("3. Exit")
    else:
        print("2. Exit")
    
    return input("\nChoice: ").strip()


def game_menu(player, world):
    """Display in-game menu"""
    print("\n" + "="*50)
    print("GAME MENU")
    print("="*50)
    print("1. Explore current area")
    print("2. Travel to another location")
    print("3. View Status")
    print("4. View Inventory")
    print("5. Save Game")
    print("6. Return to Main Menu")
    
    return input("\nChoice: ").strip()


def view_inventory(player):
    """View and manage inventory"""
    while True:
        print("\n" + "="*50)
        print("INVENTORY")
        print("="*50)
        
        if not player.inventory:
            print("Your inventory is empty.")
        else:
            for i, item in enumerate(player.inventory, 1):
                print(f"{i}. {item.name} - {item.description}")
        
        print("\nEquipped:")
        for slot, item in player.equipped.items():
            if item:
                print(f"  {slot.capitalize()}: {item.name}")
            else:
                print(f"  {slot.capitalize()}: None")
        
        print(f"\nGold: {player.gold}")
        
        print("\nOptions:")
        print("1. Use/Equip item")
        print("2. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1" and player.inventory:
            try:
                idx = int(input("Enter item number: ")) - 1
                if 0 <= idx < len(player.inventory):
                    item = player.inventory[idx]
                    
                    if item.item_type == "consumable":
                        success, message = item.use(player)
                        print(f"\n{message}")
                        if success:
                            player.remove_item(item)
                    elif item.item_type in ["weapon", "armor", "accessory"]:
                        if player.equip_item(item):
                            print(f"\nEquipped {item.name}!")
                        else:
                            print("\nCannot equip this item!")
                    else:
                        print("\nCannot use this item!")
                else:
                    print("\nInvalid item number!")
            except (ValueError, IndexError):
                print("\nInvalid input!")
            
            input("\nPress Enter to continue...")
        elif choice == "2":
            break


def travel_menu(world, player):
    """Display travel menu"""
    print("\n" + "="*50)
    print("TRAVEL")
    print("="*50)
    
    locations = world.get_available_locations()
    for i, (key, name) in enumerate(locations, 1):
        print(f"{i}. {name}")
    print(f"{len(locations) + 1}. Cancel")
    
    choice = input("\nWhere do you want to go? ").strip()
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(locations):
            location_key, location_name = locations[idx]
            world.move_to(location_key, player)
            return True
    except (ValueError, IndexError):
        pass
    
    return False


def game_loop(player, world):
    """Main game loop"""
    world.get_current_location().enter(player)
    
    while True:
        if not player.is_alive():
            print("\n💀 GAME OVER 💀")
            print("You have been defeated...")
            input("\nPress Enter to return to main menu...")
            return
        
        choice = game_menu(player, world)
        
        if choice == "1":
            # Explore
            if not world.explore(player):
                # Player was defeated
                print("\n💀 GAME OVER 💀")
                input("\nPress Enter to return to main menu...")
                return
        
        elif choice == "2":
            # Travel
            travel_menu(world, player)
        
        elif choice == "3":
            # View status
            print(player.get_status())
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            # View inventory
            view_inventory(player)
        
        elif choice == "5":
            # Save game
            if save_game(player, world):
                print("\n💾 Game saved successfully!")
            else:
                print("\n❌ Failed to save game!")
            input("\nPress Enter to continue...")
        
        elif choice == "6":
            # Return to main menu
            print("\nReturning to main menu...")
            confirm = input("Save before exiting? (y/n): ").strip().lower()
            if confirm == 'y':
                save_game(player, world)
                print("Game saved!")
            return
        
        else:
            print("\nInvalid choice!")


def main():
    """Main game function"""
    display_title()
    
    while True:
        choice = main_menu()
        
        if choice == "1":
            # New Game
            player = create_character()
            world = GameWorld()
            game_loop(player, world)
        
        elif choice == "2":
            if has_save_file():
                # Load Game
                print("\n📂 Loading saved game...")
                player, world = load_game()
                
                if player and world:
                    print("Game loaded successfully!")
                    game_loop(player, world)
                else:
                    print("Failed to load game!")
                    input("\nPress Enter to continue...")
            else:
                # Exit
                print("\n👋 Thanks for playing!")
                sys.exit(0)
        
        elif choice == "3" and has_save_file():
            # Exit
            print("\n👋 Thanks for playing!")
            sys.exit(0)
        
        else:
            print("\nInvalid choice!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing!")
        sys.exit(0)
