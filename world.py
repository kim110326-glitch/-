"""
Game world and locations for RPG game
"""
import random
from combat import start_combat
from items import create_item


class Location:
    """A location in the game world"""
    
    def __init__(self, name, description, enemies=None, items=None):
        self.name = name
        self.description = description
        self.enemies = enemies or []
        self.items = items or []
        self.visited = False
    
    def enter(self, player):
        """Enter this location"""
        if not self.visited:
            print(f"\n{'='*50}")
            print(f"📍 {self.name}")
            print(f"{'='*50}")
            print(self.description)
            self.visited = True
        else:
            print(f"\n📍 You are in {self.name}")


class GameWorld:
    """The game world containing all locations"""
    
    def __init__(self):
        self.locations = self._create_locations()
        self.current_location = "village"
    
    def _create_locations(self):
        """Create all game locations"""
        return {
            'village': Location(
                name="Peaceful Village",
                description="A quiet village where your adventure begins. The villagers speak of monsters in the nearby areas.",
                enemies=[],
                items=['health_potion']
            ),
            'forest': Location(
                name="Dark Forest",
                description="A dense forest filled with strange creatures. You can hear rustling in the bushes.",
                enemies=['slime', 'goblin'],
                items=['health_potion', 'mana_potion']
            ),
            'cave': Location(
                name="Mysterious Cave",
                description="A dark cave with glowing crystals. Dangerous creatures lurk in the shadows.",
                enemies=['goblin', 'orc'],
                items=['iron_sword', 'leather_armor']
            ),
            'mountain': Location(
                name="Rocky Mountain",
                description="A treacherous mountain path. The air is thin and cold here.",
                enemies=['orc'],
                items=['steel_sword', 'mana_potion']
            ),
            'dungeon': Location(
                name="Ancient Dungeon",
                description="An ancient dungeon filled with powerful monsters. Few have returned from here.",
                enemies=['orc', 'dragon'],
                items=['steel_armor', 'health_potion', 'mana_potion']
            ),
        }
    
    def get_current_location(self):
        """Get the current location object"""
        return self.locations[self.current_location]
    
    def explore(self, player):
        """Explore the current location"""
        location = self.get_current_location()
        
        print("\n🔍 Exploring the area...")
        
        # Random chance of finding items
        if random.random() < 0.3 and location.items:
            item_key = random.choice(location.items)
            item = create_item(item_key)
            if item:
                player.add_item(item)
                print(f"You found a {item.name}!")
        
        # Random chance of encountering enemies
        if location.enemies and random.random() < 0.6:
            enemy_type = random.choice(location.enemies)
            result = start_combat(player, enemy_type)
            
            if result is False:  # Player defeated
                return False
            elif result is True:  # Victory
                # Chance to find item after battle
                if random.random() < 0.4 and location.items:
                    item_key = random.choice(location.items)
                    item = create_item(item_key)
                    if item:
                        player.add_item(item)
                        print(f"After the battle, you found a {item.name}!")
        else:
            print("Nothing interesting happens...")
        
        return True
    
    def move_to(self, location_key, player):
        """Move to a different location"""
        if location_key in self.locations:
            self.current_location = location_key
            self.locations[location_key].enter(player)
            return True
        return False
    
    def get_available_locations(self):
        """Get list of available locations to travel to"""
        locations = []
        for key, location in self.locations.items():
            if key != self.current_location:
                locations.append((key, location.name))
        return locations
