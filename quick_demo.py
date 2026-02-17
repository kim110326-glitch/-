#!/usr/bin/env python3
"""
Quick game demonstration - automated playthrough
"""
from character import Player
from combat import create_enemy, start_combat
from world import GameWorld
from items import create_item
import time


def print_separator():
    print("\n" + "="*60)


def demo_gameplay():
    """Demonstrate a quick gameplay session"""
    
    print_separator()
    print("🎮 RPG GAME - QUICK PLAYTHROUGH DEMO")
    print_separator()
    
    # Create character
    print("\n📝 Creating character...")
    player = Player("Hero", "Warrior")
    print(f"✨ {player.name} the {player.char_class} has been created!")
    print(player.get_status())
    
    # Give some starting items
    player.add_item(create_item('health_potion'))
    player.add_item(create_item('health_potion'))
    print("\n🎒 Starting inventory: 2x Health Potions")
    
    # Create world
    world = GameWorld()
    print(f"\n📍 Starting in: {world.get_current_location().name}")
    
    # First combat
    print_separator()
    print("⚔️  ENCOUNTER 1: Fighting a Slime")
    print_separator()
    
    enemy = create_enemy("slime", player.level)
    print(f"\nA wild {enemy.name} appears!")
    print(f"Enemy stats: HP={enemy.max_hp}, Attack={enemy.attack}, Defense={enemy.defense}")
    
    print("\n--- Combat ---")
    while enemy.is_alive() and player.is_alive():
        damage = player.basic_attack(enemy)
        print(f"{player.name} attacks for {damage} damage! ({enemy.name} HP: {enemy.hp}/{enemy.max_hp})")
        
        if enemy.is_alive():
            enemy_damage = enemy.basic_attack(player)
            print(f"{enemy.name} attacks for {enemy_damage} damage! ({player.name} HP: {player.hp}/{player.max_hp})")
    
    if player.is_alive():
        print(f"\n🎉 Victory! {enemy.name} defeated!")
        leveled = player.gain_experience(enemy.exp_reward)
        player.gold += enemy.gold_reward
        print(f"Gained {enemy.exp_reward} EXP and {enemy.gold_reward} gold!")
        
        if leveled:
            print(f"⭐ LEVEL UP! Now Level {player.level}")
    
    # Find item
    print_separator()
    print("🔍 EXPLORATION")
    print_separator()
    
    sword = create_item('iron_sword')
    player.add_item(sword)
    print(f"\nFound an {sword.name}!")
    print(f"Equipping {sword.name}...")
    player.equip_item(sword)
    print(f"Attack increased to {player.attack}!")
    
    # Travel to new location
    print("\n🚶 Traveling to Dark Forest...")
    world.move_to("forest", player)
    
    # Second combat (harder)
    print_separator()
    print("⚔️  ENCOUNTER 2: Fighting a Goblin")
    print_separator()
    
    enemy = create_enemy("goblin", player.level)
    print(f"\nA wild {enemy.name} appears!")
    print(f"Enemy stats: HP={enemy.max_hp}, Attack={enemy.attack}, Defense={enemy.defense}")
    
    print("\n--- Combat ---")
    rounds = 0
    while enemy.is_alive() and player.is_alive() and rounds < 5:
        rounds += 1
        damage = player.basic_attack(enemy)
        print(f"{player.name} attacks for {damage} damage! ({enemy.name} HP: {enemy.hp}/{enemy.max_hp})")
        
        if enemy.is_alive():
            enemy_damage = enemy.basic_attack(player)
            print(f"{enemy.name} attacks for {enemy_damage} damage! ({player.name} HP: {player.hp}/{player.max_hp})")
            
            # Use potion if health is low
            if player.hp < player.max_hp * 0.5 and player.inventory:
                for item in player.inventory:
                    if item.name == "Health Potion":
                        success, msg = item.use(player)
                        print(f"💊 Used Health Potion! {msg}")
                        player.remove_item(item)
                        break
    
    if player.is_alive() and not enemy.is_alive():
        print(f"\n🎉 Victory! {enemy.name} defeated!")
        leveled = player.gain_experience(enemy.exp_reward)
        player.gold += enemy.gold_reward
        print(f"Gained {enemy.exp_reward} EXP and {enemy.gold_reward} gold!")
        
        if leveled:
            print(f"⭐ LEVEL UP! Now Level {player.level}")
    
    # Final status
    print_separator()
    print("📊 FINAL STATUS")
    print_separator()
    print(player.get_status())
    print(f"\nEquipped:")
    for slot, item in player.equipped.items():
        if item:
            print(f"  {slot.capitalize()}: {item.name}")
    
    print_separator()
    print("✨ Demo Complete!")
    print_separator()
    print("\nThis demonstrates:")
    print("✓ Character creation and stats")
    print("✓ Turn-based combat system")
    print("✓ Experience and leveling")
    print("✓ Item collection and usage")
    print("✓ Equipment system")
    print("✓ World exploration")
    print("\nTo play the full game, run: python3 rpg_game.py")


if __name__ == "__main__":
    demo_gameplay()
