"""
Combat system for RPG game
"""
import random
from character import Enemy


def create_enemy(enemy_type, player_level):
    """Create an enemy based on type and player level"""
    level = max(1, player_level + random.randint(-1, 1))
    
    if enemy_type == "slime":
        return Enemy(
            name="Slime",
            hp=20 + (level * 5),
            mp=5,
            attack=5 + level,
            defense=2 + level,
            level=level,
            exp_reward=10 + (level * 5),
            gold_reward=5 + (level * 3)
        )
    elif enemy_type == "goblin":
        return Enemy(
            name="Goblin",
            hp=30 + (level * 8),
            mp=10,
            attack=8 + (level * 2),
            defense=4 + level,
            level=level,
            exp_reward=20 + (level * 8),
            gold_reward=10 + (level * 5)
        )
    elif enemy_type == "orc":
        return Enemy(
            name="Orc",
            hp=50 + (level * 10),
            mp=15,
            attack=12 + (level * 2),
            defense=6 + (level * 2),
            level=level,
            exp_reward=30 + (level * 10),
            gold_reward=15 + (level * 7)
        )
    elif enemy_type == "dragon":
        return Enemy(
            name="Dragon",
            hp=100 + (level * 20),
            mp=30,
            attack=20 + (level * 3),
            defense=10 + (level * 2),
            level=level,
            exp_reward=100 + (level * 20),
            gold_reward=50 + (level * 15)
        )
    else:
        return Enemy(
            name="Unknown Enemy",
            hp=30,
            mp=10,
            attack=8,
            defense=3,
            level=1,
            exp_reward=15,
            gold_reward=10
        )


def combat_turn(player, enemy):
    """Execute one turn of combat"""
    print(f"\n{'='*50}")
    print(f"{player.name} HP: {player.hp}/{player.max_hp}  |  {enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
    print(f"{'='*50}")
    
    print("\nWhat will you do?")
    print("1. Attack")
    print("2. Use Skill")
    print("3. Use Item")
    print("4. Run")
    
    choice = input("\nChoice: ").strip()
    
    if choice == "1":
        # Player attacks
        damage = player.basic_attack(enemy)
        print(f"\n{player.name} attacks {enemy.name} for {damage} damage!")
        
    elif choice == "2":
        # Use skill
        print("\nAvailable Skills:")
        if player.char_class == "Warrior":
            print("1. Power Attack (10 MP) - Deal heavy damage")
        elif player.char_class == "Mage":
            print("1. Fireball (15 MP) - Deal magic damage")
        print("2. Heal (12 MP) - Restore your HP")
        print("3. Cancel")
        
        skill_choice = input("\nChoice: ").strip()
        
        if skill_choice == "1":
            if player.char_class == "Warrior":
                result, skill_name = player.use_skill("Power Attack", enemy)
                if skill_name != "Failed":
                    print(f"\n{player.name} uses {skill_name}! Deals {result} damage!")
                else:
                    print("\nNot enough MP!")
                    return combat_turn(player, enemy)
            elif player.char_class == "Mage":
                result, skill_name = player.use_skill("Fireball", enemy)
                if skill_name != "Failed":
                    print(f"\n{player.name} casts {skill_name}! Deals {result} damage!")
                else:
                    print("\nNot enough MP!")
                    return combat_turn(player, enemy)
        elif skill_choice == "2":
            result, skill_name = player.use_skill("Heal", enemy)
            if skill_name != "Failed":
                print(f"\n{player.name} uses Heal! Restores {result} HP!")
            else:
                print("\nNot enough MP!")
                return combat_turn(player, enemy)
        else:
            return combat_turn(player, enemy)
            
    elif choice == "3":
        # Use item
        if not player.inventory:
            print("\nYou have no items!")
            return combat_turn(player, enemy)
        
        print("\nInventory:")
        for i, item in enumerate(player.inventory, 1):
            print(f"{i}. {item.name} - {item.description}")
        print(f"{len(player.inventory) + 1}. Cancel")
        
        item_choice = input("\nChoice: ").strip()
        try:
            idx = int(item_choice) - 1
            if 0 <= idx < len(player.inventory):
                item = player.inventory[idx]
                if hasattr(item, 'use') and item.item_type == "consumable":
                    success, message = item.use(player)
                    if success:
                        print(f"\n{message}")
                        player.remove_item(item)
                    else:
                        print("\nCannot use this item in combat!")
                        return combat_turn(player, enemy)
                else:
                    print("\nCannot use this item in combat!")
                    return combat_turn(player, enemy)
            else:
                return combat_turn(player, enemy)
        except (ValueError, IndexError):
            return combat_turn(player, enemy)
            
    elif choice == "4":
        # Try to run
        if random.random() < 0.5:
            print("\nYou successfully escaped!")
            return "escaped"
        else:
            print("\nCouldn't escape!")
    else:
        print("\nInvalid choice!")
        return combat_turn(player, enemy)
    
    # Check if enemy is defeated
    if not enemy.is_alive():
        print(f"\n{enemy.name} has been defeated!")
        print(f"Gained {enemy.exp_reward} EXP and {enemy.gold_reward} gold!")
        
        leveled_up = player.gain_experience(enemy.exp_reward)
        player.gold += enemy.gold_reward
        
        if leveled_up:
            print(f"\n🎉 Level Up! {player.name} is now level {player.level}!")
        
        return "victory"
    
    # Enemy's turn
    enemy_damage = enemy.basic_attack(player)
    print(f"{enemy.name} attacks {player.name} for {enemy_damage} damage!")
    
    # Check if player is defeated
    if not player.is_alive():
        print(f"\n💀 {player.name} has been defeated...")
        return "defeat"
    
    input("\nPress Enter to continue...")
    return "continue"


def start_combat(player, enemy_type):
    """Start a combat encounter"""
    enemy = create_enemy(enemy_type, player.level)
    print(f"\n⚔️  A wild {enemy.name} (Level {enemy.level}) appears!")
    
    while True:
        result = combat_turn(player, enemy)
        
        if result == "victory":
            return True
        elif result == "defeat":
            return False
        elif result == "escaped":
            return None
