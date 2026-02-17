#!/usr/bin/env python3
"""
Test script for RPG game functionality
"""
import sys
from character import Player, Enemy
from items import create_item, Potion, Weapon, Armor
from combat import create_enemy
from world import GameWorld
from save_load import save_game, load_game


def test_character_creation():
    """Test character creation"""
    print("Testing character creation...")
    
    # Test Warrior
    warrior = Player("TestWarrior", "Warrior")
    assert warrior.name == "TestWarrior"
    assert warrior.char_class == "Warrior"
    assert warrior.hp > 0
    assert warrior.is_alive()
    print("✓ Warrior created successfully")
    
    # Test Mage
    mage = Player("TestMage", "Mage")
    assert mage.name == "TestMage"
    assert mage.char_class == "Mage"
    print("✓ Mage created successfully")
    
    # Test Rogue
    rogue = Player("TestRogue", "Rogue")
    assert rogue.name == "TestRogue"
    assert rogue.char_class == "Rogue"
    print("✓ Rogue created successfully")


def test_items():
    """Test item system"""
    print("\nTesting item system...")
    
    # Test potion
    potion = create_item('health_potion')
    assert potion is not None
    assert potion.name == "Health Potion"
    print("✓ Health potion created")
    
    # Test weapon
    sword = create_item('iron_sword')
    assert sword is not None
    assert sword.attack_bonus > 0
    print("✓ Iron sword created")
    
    # Test armor
    armor = create_item('leather_armor')
    assert armor is not None
    assert armor.defense_bonus > 0
    print("✓ Leather armor created")


def test_combat():
    """Test combat mechanics"""
    print("\nTesting combat mechanics...")
    
    player = Player("TestPlayer", "Warrior")
    enemy = create_enemy("slime", 1)
    
    assert enemy is not None
    assert enemy.is_alive()
    print("✓ Enemy created")
    
    # Test attack
    initial_enemy_hp = enemy.hp
    damage = player.basic_attack(enemy)
    assert damage > 0
    assert enemy.hp < initial_enemy_hp
    print("✓ Attack system works")
    
    # Test healing
    player.hp = player.max_hp - 10
    heal_amount = player.heal(10)
    assert player.hp == player.max_hp
    print("✓ Healing system works")


def test_inventory():
    """Test inventory management"""
    print("\nTesting inventory system...")
    
    player = Player("TestPlayer", "Warrior")
    
    # Add items
    potion = create_item('health_potion')
    player.add_item(potion)
    assert len(player.inventory) == 1
    print("✓ Item added to inventory")
    
    # Use item
    player.hp = player.max_hp - 20
    success, message = potion.use(player)
    assert success
    player.remove_item(potion)
    assert len(player.inventory) == 0
    print("✓ Item used and removed")
    
    # Equip weapon
    sword = create_item('iron_sword')
    player.add_item(sword)
    initial_attack = player.attack
    player.equip_item(sword)
    assert player.attack > initial_attack
    assert player.equipped['weapon'] == sword
    print("✓ Equipment system works")


def test_level_up():
    """Test leveling system"""
    print("\nTesting level system...")
    
    player = Player("TestPlayer", "Warrior")
    initial_level = player.level
    initial_stats = (player.max_hp, player.attack, player.defense)
    
    # Gain enough experience to level up
    player.gain_experience(100)
    
    assert player.level > initial_level
    assert player.max_hp > initial_stats[0]
    assert player.attack > initial_stats[1]
    assert player.defense > initial_stats[2]
    print("✓ Level up system works")


def test_world():
    """Test game world"""
    print("\nTesting game world...")
    
    world = GameWorld()
    assert world.current_location == "village"
    print("✓ World created with starting location")
    
    locations = world.get_available_locations()
    assert len(locations) > 0
    print("✓ Multiple locations available")
    
    # Test moving to a location
    first_location = locations[0][0]
    player = Player("TestPlayer", "Warrior")
    world.move_to(first_location, player)
    assert world.current_location == first_location
    print("✓ Location travel works")


def test_save_load():
    """Test save/load functionality"""
    print("\nTesting save/load system...")
    
    # Create a player and world
    player = Player("SaveTest", "Warrior")
    player.gold = 100
    player.level = 2
    
    world = GameWorld()
    world.move_to("forest", player)
    
    # Save
    success = save_game(player, world)
    assert success
    print("✓ Game saved successfully")
    
    # Load
    loaded_player, loaded_world = load_game()
    assert loaded_player is not None
    assert loaded_world is not None
    assert loaded_player.name == "SaveTest"
    assert loaded_player.gold == 100
    assert loaded_world.current_location == "forest"
    print("✓ Game loaded successfully")
    
    # Clean up
    import os
    if os.path.exists("savegame.json"):
        os.remove("savegame.json")


def main():
    """Run all tests"""
    print("="*50)
    print("RPG GAME TEST SUITE")
    print("="*50)
    
    try:
        test_character_creation()
        test_items()
        test_combat()
        test_inventory()
        test_level_up()
        test_world()
        test_save_load()
        
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("="*50)
        return 0
    
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
