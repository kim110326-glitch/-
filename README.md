# Text RPG Adventure Game

A simple text-based RPG game written in Python featuring character progression, turn-based combat, exploration, and inventory management.

## Features

- **Character Classes**: Choose from Warrior, Mage, or Rogue
- **Turn-based Combat**: Fight against various enemies (Slimes, Goblins, Orcs, Dragons)
- **Character Progression**: Gain experience, level up, and improve your stats
- **Inventory System**: Collect items, potions, weapons, and armor
- **Equipment System**: Equip weapons and armor to boost your stats
- **Multiple Locations**: Explore different areas including forests, caves, mountains, and dungeons
- **Save/Load System**: Save your progress and continue later

## How to Play

### Installation

1. Make sure you have Python 3.6 or higher installed
2. Clone this repository
3. Run the game:
   ```bash
   python rpg_game.py
   ```

### Game Controls

The game is menu-driven. Simply enter the number corresponding to your choice.

### Character Classes

- **Warrior**: High HP and Attack, ideal for direct combat
- **Mage**: High MP and magic abilities, powerful spells
- **Rogue**: Balanced stats, versatile playstyle

### Combat System

During combat, you can:
- **Attack**: Perform a basic attack
- **Use Skill**: Use class-specific abilities (costs MP)
  - Warrior: Power Attack (heavy damage)
  - Mage: Fireball (magic damage)
  - All: Heal (restore HP)
- **Use Item**: Use consumable items from inventory
- **Run**: Attempt to escape from battle

### Items

- **Health Potion**: Restores 30 HP
- **Mana Potion**: Restores 20 MP
- **Iron Sword**: +5 Attack
- **Steel Sword**: +10 Attack
- **Leather Armor**: +5 Defense
- **Steel Armor**: +10 Defense

### Locations

- **Peaceful Village**: Safe starting area
- **Dark Forest**: Home to slimes and goblins
- **Mysterious Cave**: More dangerous enemies and better loot
- **Rocky Mountain**: Challenging terrain with orcs
- **Ancient Dungeon**: The most dangerous area with powerful enemies

## Game Files

- `rpg_game.py`: Main game entry point
- `character.py`: Character classes (Player, Enemy)
- `combat.py`: Combat system
- `items.py`: Items and equipment
- `world.py`: Game world and locations
- `save_load.py`: Save/load functionality

## Tips

- Explore areas to find items and gold
- Save your game frequently
- Use potions wisely during combat
- Equip better weapons and armor as you find them
- Level up by defeating enemies
- Start with easier areas before attempting the dungeon

## License

This project is open source and available for educational purposes.