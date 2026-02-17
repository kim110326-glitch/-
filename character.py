"""
Character class for RPG game
"""
import random


class Character:
    """Base character class for player and enemies"""
    
    def __init__(self, name, hp, mp, attack, defense, level=1):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.experience = 0
        self.gold = 0
        self.inventory = []
        self.equipped = {
            'weapon': None,
            'armor': None,
            'accessory': None
        }
    
    def is_alive(self):
        """Check if character is alive"""
        return self.hp > 0
    
    def take_damage(self, damage):
        """Take damage from an attack"""
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        if self.hp < 0:
            self.hp = 0
        return actual_damage
    
    def heal(self, amount):
        """Heal HP"""
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        return amount
    
    def restore_mp(self, amount):
        """Restore MP"""
        self.mp += amount
        if self.mp > self.max_mp:
            self.mp = self.max_mp
        return amount
    
    def basic_attack(self, target):
        """Perform basic attack on target"""
        damage = random.randint(self.attack - 2, self.attack + 2)
        actual_damage = target.take_damage(damage)
        return actual_damage
    
    def add_item(self, item):
        """Add item to inventory"""
        self.inventory.append(item)
    
    def remove_item(self, item):
        """Remove item from inventory"""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def equip_item(self, item):
        """Equip an item"""
        if item.item_type in self.equipped:
            # Unequip current item
            if self.equipped[item.item_type]:
                self.unequip_item(item.item_type)
            
            # Equip new item
            self.equipped[item.item_type] = item
            self.attack += item.attack_bonus
            self.defense += item.defense_bonus
            self.remove_item(item)
            return True
        return False
    
    def unequip_item(self, slot):
        """Unequip an item"""
        if self.equipped[slot]:
            item = self.equipped[slot]
            self.attack -= item.attack_bonus
            self.defense -= item.defense_bonus
            self.add_item(item)
            self.equipped[slot] = None
            return True
        return False
    
    def gain_experience(self, exp):
        """Gain experience and level up if needed"""
        self.experience += exp
        exp_needed = self.level * 100
        
        if self.experience >= exp_needed:
            self.level_up()
            return True
        return False
    
    def level_up(self):
        """Level up the character"""
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.max_mp += 5
        self.mp = self.max_mp
        self.attack += 3
        self.defense += 2
        self.experience = 0
    
    def get_status(self):
        """Get character status string"""
        status = f"\n{self.name} (Level {self.level})\n"
        status += f"HP: {self.hp}/{self.max_hp}\n"
        status += f"MP: {self.mp}/{self.max_mp}\n"
        status += f"Attack: {self.attack}\n"
        status += f"Defense: {self.defense}\n"
        status += f"Experience: {self.experience}/{self.level * 100}\n"
        status += f"Gold: {self.gold}\n"
        return status


class Player(Character):
    """Player character class"""
    
    def __init__(self, name, char_class="Warrior"):
        self.char_class = char_class
        
        # Set stats based on class
        if char_class == "Warrior":
            super().__init__(name, hp=100, mp=20, attack=15, defense=10)
        elif char_class == "Mage":
            super().__init__(name, hp=60, mp=50, attack=8, defense=5)
        elif char_class == "Rogue":
            super().__init__(name, hp=80, mp=30, attack=12, defense=7)
        else:
            super().__init__(name, hp=80, mp=30, attack=10, defense=8)
    
    def use_skill(self, skill_name, target):
        """Use a skill"""
        if skill_name == "Power Attack" and self.mp >= 10:
            self.mp -= 10
            damage = random.randint(self.attack * 2, self.attack * 3)
            actual_damage = target.take_damage(damage)
            return actual_damage, "Power Attack"
        
        elif skill_name == "Fireball" and self.mp >= 15:
            self.mp -= 15
            damage = random.randint(20, 30)
            actual_damage = target.take_damage(damage)
            return actual_damage, "Fireball"
        
        elif skill_name == "Heal" and self.mp >= 12:
            self.mp -= 12
            heal_amount = random.randint(20, 30)
            actual_heal = self.heal(heal_amount)
            return actual_heal, "Heal"
        
        return 0, "Failed"


class Enemy(Character):
    """Enemy character class"""
    
    def __init__(self, name, hp, mp, attack, defense, level, exp_reward, gold_reward):
        super().__init__(name, hp, mp, attack, defense, level)
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
