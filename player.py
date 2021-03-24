import enum
import math

# Possible player classes
# Use eg: player.PlayerClass.Arquero(10, 20)
class PlayerClass(enum.Enum):
    class ClassType(object):
        def __init__(self, attack_mult, defense_mult):
            self.attack_mult = attack_mult
            self.defense_mult = defense_mult
        
        def fitness(self, attack, defense):
            return self.attack_mult * attack + self.defense_mult * defense
            
    Guerrero = ClassType(0.6, 0.6).fitness
    Arquero = ClassType(0.9, 0.1).fitness
    Defensor = ClassType(0.3, 0.8).fitness
    Infiltrado = ClassType(0.8, 0.3).fitness

class EquipmentType(enum.Enum):
    Weapon = "\U0001F3F9"
    Boots = "\U0001FA74"
    Helmet = "\U0001FA96"
    Gloves = "\U0001F9E4"
    Armor = "\U0001F9BA"

class Stats(object):
    def __init__(self, strength, agility, expertise, resistance, life):
        """Returns a Stats object with the given stats

        Parameters
        ----------
        strength : double
            Equipment stat value
        agility : double
            Equipment stat value
        expertise : double
            Equipment stat value
        resistance : double
            Equipment stat value
        life : double
            Equipment stat value
        """

        self.strength = strength
        self.agility = agility
        self.expertise = expertise
        self.resistance = resistance
        self.life = life
    
    def add_stats(self, other_stats):
        self.strength += other_stats.strength
        self.agility += other_stats.agility
        self.expertise += other_stats.expertise
        self.resistance += other_stats.resistance
        self.life += other_stats.life

class Equipment(object):
    def __init__(self, equipment_type, id, stats):
        """Returns an Equipment object with the given stats

        Parameters
        ----------
        equipment_type : EquipmentType
            Type of equipment
        id : int
            Equipment id
        stats : Stats
            Equipment stats
        """

        self.equipment_type = equipment_type
        self.id = id
        self.stats = stats

class Player(object):
    def __init__(self, player_class, height, weapon, boots, helmet, gloves, armor):
        """Returns a Player object with the given height and equipments

        Parameters
        ----------
        player_class : PlayerClass
            Type of player
        height : double
            Player height
        weapon : Equipment
            Player equipped weapon
        boots : Equipment
            Player equipped boots
        helmet : Equipment
            Player equipped helmet
        gloves : Equipment
            Player equipped gloves
        armor : Equipment
            Player equipped armor
        """
        
        self.player_class = player_class
        self.height = height
        # TODO: Check si vale la pena hacer los chequeos de equipment_type
        # TODO: Check si vale la pena guardarlos por separado, no en un array
        if weapon.equipment_type != EquipmentType.Weapon:
            raise ValueError("Not a weapon!")
        self.weapon = weapon

        if boots.equipment_type != EquipmentType.Boots:
            raise ValueError("Not boots!")
        self.boots = boots

        if helmet.equipment_type != EquipmentType.Helmet:
            raise ValueError("Not a helmet!")
        self.helmet = helmet

        if gloves.equipment_type != EquipmentType.Gloves:
            raise ValueError("Not gloves!")
        self.gloves = gloves

        if armor.equipment_type != EquipmentType.Armor:
            raise ValueError("Not an armor!")
        self.armor = armor

        # Initialize stat saved values to None, will be calculated and stored on demand
        # TODO: Check si me sirve guardar todas, puedo sino guardar solo fitness
        self.player_stats = None
        self.attack_mod = None
        self.defense_mod = None
        self.attack = None
        self.defense = None
        self.s_fitness = None
    
    def player_stats(self):
        # Player Stats is an object, no need to add is not None to condition
        if self.player_stats:
            return self.player_stats

        # Accumulate item stats
        total_item_stats = Stats(0, 0, 0, 0, 0)
        for item in [self.weapon, self.boots, self.helmet, self.gloves, self.armor]:
            total_item_stats.add_stats(item.stats)
        
        # Calculate player stats
        self.player_stats = Stats(
            100 * math.tanh(0.01 * total_item_stats.strength),
            math.tanh(0.01 * total_item_stats.agility),
            0.6 * math.tanh(0.01 * total_item_stats.expertise),
            math.tanh(0.01 * total_item_stats.resistance),
            100 * math.tanh(0.01 * total_item_stats.life))
        
        return self.player_stats
    
    def height_modifiers(self):
        # Check for None as modifiers could be 0
        if self.attack_mod is not None and self.defense_mod is not None:
            return (self.attack_mod, self.defense_mod)
    
        # Calculate height modifiers
        self.attack_mod = 0.7 - math.pow(3 * self.height - 5, 4) + math.pow(3 * self.height - 5, 2) + self.height / 4
        self.defense_mod = 1.9 + math.pow(2.5 * self.height - 4.16, 4) - math.pow(2.5 * self.height - 4.16, 2) - 3 * self.height / 10

        return (self.attack_mod, self.defense_mod)
    
    def final_stats(self):
        # Check for None as final stats could be 0
        if self.attack is not None and self.defense is not None:
            return (self.attack, self.defense)
    
        # Set player stats if not done before
        self.player_stats()
        # Set height modifiers if not done before
        self.height_modifiers()

        self.attack = (self.player_stats.agility + self.player_stats.expertise) * self.player_stats.strength * self.attack_mod
        self.defense = (self.player_stats.resistance + self.player_stats.expertise) * self.player_stats.life * self.defense_mod

        return (self.attack, self.defense)
    
    def fitness(self):
        # Check for None as fitness could be 0
        if self.s_fitness is not None:
            return self.s_fitness

        # Set final stats if not done before
        self.final_stats()

        self.s_fitness = self.player_class(self.attack, self.defense)

        return self.s_fitness

