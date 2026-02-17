#!/usr/bin/env python3
"""
Demo script to showcase RPG game features
"""
import sys
from character import Player
from items import create_item
from combat import create_enemy
from world import GameWorld


def demo_character_system():
    """Demonstrate character system"""
    print("\n" + "="*60)
    print("DEMO: Character System")
    print("="*60)
    
    # Create different classes
    warrior = Player("Warrior", "Warrior")
    mage = Player("Mage", "Mage")
    rogue = Player("Rogue", "Rogue")
    
    print("\nCreated three character classes:")
    for char in [warrior, mage, rogue]:
        print(char.get_status())


def demo_combat_system():
    """Demonstrate combat system"""
    print("\n" + "="*60)
    print("DEMO: Combat System")
    print("="*60)
    
    player = Player("Hero", "Warrior")
    enemy = create_enemy("slime", 1)
    
    print(f"\n{player.name} encounters a {enemy.name}!")
    print(f"Player: HP={player.hp}, Attack={player.attack}")
    print(f"Enemy: HP={enemy.hp}, Attack={enemy.attack}")
    
    # Simulate a few combat rounds
    print("\n--- Combat Round 1 ---")
    damage = player.basic_attack(enemy)
    print(f"{player.name} attacks for {damage} damage!")
    print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
    
    enemy_damage = enemy.basic_attack(player)
    print(f"{enemy.name} attacks for {enemy_damage} damage!")
    print(f"{player.name} HP: {player.hp}/{player.max_hp}")


def demo_inventory_system():
    """Demonstrate inventory and equipment"""
    print("\n" + "="*60)
    print("DEMO: Inventory & Equipment System")
    print("="*60)
    
    player = Player("Hero", "Warrior")
    
    print(f"\nInitial stats: Attack={player.attack}, Defense={player.defense}")
    
    # Add items
    sword = create_item('iron_sword')
    armor = create_item('leather_armor')
    potion = create_item('health_potion')
    
    player.add_item(sword)
    player.add_item(armor)
    player.add_item(potion)
    
    print(f"\nInventory: {[item.name for item in player.inventory]}")
    
    # Equip items
    player.equip_item(sword)
    print(f"\nEquipped {sword.name}")
    print(f"New Attack: {player.attack} (+{sword.attack_bonus})")
    
    player.equip_item(armor)
    print(f"\nEquipped {armor.name}")
    print(f"New Defense: {player.defense} (+{armor.defense_bonus})")
    
    # Use potion
    player.hp = 50
    print(f"\nPlayer HP before potion: {player.hp}/{player.max_hp}")
    success, message = potion.use(player)
    print(message)
    print(f"Player HP after potion: {player.hp}/{player.max_hp}")


def demo_leveling_system():
    """Demonstrate leveling system"""
    print("\n" + "="*60)
    print("DEMO: Leveling System")
    print("="*60)
    
    player = Player("Hero", "Warrior")
    
    print(f"\nLevel {player.level} stats:")
    print(f"HP: {player.max_hp}, Attack: {player.attack}, Defense: {player.defense}")
    
    # Gain experience
    print("\nGaining experience from battles...")
    player.gain_experience(50)
    print(f"Experience: {player.experience}/100")
    
    player.gain_experience(50)
    print(f"Experience: {player.experience}/100")
    
    print(f"\n🎉 Level Up! Now Level {player.level}")
    print(f"New HP: {player.max_hp}, Attack: {player.attack}, Defense: {player.defense}")


def demo_world_system():
    """Demonstrate world and locations"""
    print("\n" + "="*60)
    print("DEMO: World & Exploration System")
    print("="*60)
    
    world = GameWorld()
    player = Player("Hero", "Warrior")
    
    print(f"\nStarting location: {world.get_current_location().name}")
    
    print("\nAvailable locations to explore:")
    for key, name in world.get_available_locations():
        loc = world.locations[key]
        print(f"  • {name}")
        print(f"    Enemies: {', '.join(loc.enemies) if loc.enemies else 'None'}")
        print(f"    Items: {', '.join(loc.items) if loc.items else 'None'}")


def demo_enemy_types():
    """Demonstrate different enemy types"""
    print("\n" + "="*60)
    print("DEMO: Enemy Types")
    print("="*60)
    
    enemy_types = ["slime", "goblin", "orc", "dragon"]
    
    print("\nEnemy progression:")
    for enemy_type in enemy_types:
        enemy = create_enemy(enemy_type, 1)
        print(f"\n{enemy.name} (Level {enemy.level}):")
        print(f"  HP: {enemy.max_hp}")
        print(f"  Attack: {enemy.attack}")
        print(f"  Defense: {enemy.defense}")
        print(f"  Rewards: {enemy.exp_reward} EXP, {enemy.gold_reward} Gold")


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("🎮 RPG GAME FEATURE DEMONSTRATION")
    print("="*60)
    
    demo_character_system()
    demo_combat_system()
    demo_inventory_system()
    demo_leveling_system()
    demo_world_system()
    demo_enemy_types()
    
    print("\n" + "="*60)
    print("✨ Demo Complete!")
    print("="*60)
    print("\nTo play the game, run: python3 rpg_game.py")


if __name__ == "__main__":
    main()
