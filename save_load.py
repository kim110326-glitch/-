"""
Save and load game functionality
"""
import json
import os
from character import Player
from items import create_item


SAVE_FILE = "savegame.json"


def save_game(player, world):
    """Save the current game state"""
    save_data = {
        'player': {
            'name': player.name,
            'char_class': player.char_class,
            'hp': player.hp,
            'max_hp': player.max_hp,
            'mp': player.mp,
            'max_mp': player.max_mp,
            'attack': player.attack,
            'defense': player.defense,
            'level': player.level,
            'experience': player.experience,
            'gold': player.gold,
            'inventory': [item.name for item in player.inventory],
            'equipped': {
                slot: item.name if item else None 
                for slot, item in player.equipped.items()
            }
        },
        'world': {
            'current_location': world.current_location,
            'visited_locations': [
                key for key, loc in world.locations.items() if loc.visited
            ]
        }
    }
    
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(save_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False


def load_game():
    """Load a saved game"""
    if not os.path.exists(SAVE_FILE):
        return None, None
    
    try:
        with open(SAVE_FILE, 'r') as f:
            save_data = json.load(f)
        
        # Restore player
        player_data = save_data['player']
        player = Player(player_data['name'], player_data['char_class'])
        
        player.hp = player_data['hp']
        player.max_hp = player_data['max_hp']
        player.mp = player_data['mp']
        player.max_mp = player_data['max_mp']
        player.attack = player_data['attack']
        player.defense = player_data['defense']
        player.level = player_data['level']
        player.experience = player_data['experience']
        player.gold = player_data['gold']
        
        # Restore inventory (simplified - just names)
        player.inventory = []
        for item_name in player_data['inventory']:
            # Try to match item name to create it
            for key, item_template in __import__('items').ITEMS.items():
                if item_template.name == item_name:
                    item = create_item(key)
                    if item:
                        player.inventory.append(item)
                    break
        
        # Restore world state
        from world import GameWorld
        world = GameWorld()
        world_data = save_data['world']
        world.current_location = world_data['current_location']
        
        for loc_key in world_data['visited_locations']:
            if loc_key in world.locations:
                world.locations[loc_key].visited = True
        
        return player, world
    
    except Exception as e:
        print(f"Error loading game: {e}")
        return None, None


def has_save_file():
    """Check if a save file exists"""
    return os.path.exists(SAVE_FILE)
