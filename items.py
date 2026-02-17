"""
Items and equipment for RPG game
"""


class Item:
    """Base item class"""
    
    def __init__(self, name, description, item_type="consumable"):
        self.name = name
        self.description = description
        self.item_type = item_type
    
    def use(self, target):
        """Use the item on a target"""
        return False


class Potion(Item):
    """Health potion"""
    
    def __init__(self, name="Health Potion", heal_amount=30):
        super().__init__(name, f"Restores {heal_amount} HP", "consumable")
        self.heal_amount = heal_amount
    
    def use(self, target):
        """Use potion to heal target"""
        actual_heal = target.heal(self.heal_amount)
        return True, f"Restored {actual_heal} HP!"


class ManaPotion(Item):
    """Mana potion"""
    
    def __init__(self, name="Mana Potion", restore_amount=20):
        super().__init__(name, f"Restores {restore_amount} MP", "consumable")
        self.restore_amount = restore_amount
    
    def use(self, target):
        """Use potion to restore MP"""
        actual_restore = target.restore_mp(self.restore_amount)
        return True, f"Restored {actual_restore} MP!"


class Equipment(Item):
    """Base equipment class"""
    
    def __init__(self, name, description, item_type, attack_bonus=0, defense_bonus=0):
        super().__init__(name, description, item_type)
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus


class Weapon(Equipment):
    """Weapon equipment"""
    
    def __init__(self, name, description, attack_bonus):
        super().__init__(name, description, "weapon", attack_bonus=attack_bonus)


class Armor(Equipment):
    """Armor equipment"""
    
    def __init__(self, name, description, defense_bonus):
        super().__init__(name, description, "armor", defense_bonus=defense_bonus)


# Predefined items
ITEMS = {
    'health_potion': Potion("Health Potion", 30),
    'mana_potion': ManaPotion("Mana Potion", 20),
    'iron_sword': Weapon("Iron Sword", "A sturdy iron sword", 5),
    'steel_sword': Weapon("Steel Sword", "A sharp steel sword", 10),
    'leather_armor': Armor("Leather Armor", "Basic leather protection", 5),
    'steel_armor': Armor("Steel Armor", "Heavy steel armor", 10),
}


def create_item(item_key):
    """Create a new instance of an item"""
    if item_key in ITEMS:
        item_template = ITEMS[item_key]
        if isinstance(item_template, Potion):
            return Potion(item_template.name, item_template.heal_amount)
        elif isinstance(item_template, ManaPotion):
            return ManaPotion(item_template.name, item_template.restore_amount)
        elif isinstance(item_template, Weapon):
            return Weapon(item_template.name, item_template.description, item_template.attack_bonus)
        elif isinstance(item_template, Armor):
            return Armor(item_template.name, item_template.description, item_template.defense_bonus)
    return None
