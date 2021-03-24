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
    Weapon = "🏹"
    Boots = "🥾"
    Helmet = "⛑"
    Gloves = "🧤"
    Armor = "🦺"

class Stats(object):
    def __init__(self, strength, agility, expertise, resistance, life):
        """Returns a Stats object with the given stats

        Parameters
        ----------
        strength : float
            Equipment stat value
        agility : float
            Equipment stat value
        expertise : float
            Equipment stat value
        resistance : float
            Equipment stat value
        life : float
            Equipment stat value
        """

        self.strength = strength
        self.agility = agility
        self.expertise = expertise
        self.resistance = resistance
        self.life = life
    
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Stats(strength=%s,agility=%s,expertise=%s,resistance=%s,life=%s)" % (self.strength, self.agility, self.expertise, self.resistance, self.life)

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

    @classmethod
    def new_from_row(cls, equipment_type, row):
        """Returns an Equipment object with the given row

        Parameters
        ----------
        equipment_type : EquipmentType
            Type of equipment
        row : list of strings
            Row from tsv. Expected order is ['id', 'Fu', 'Ag', 'Ex', 'Re', 'Vi']
        """
        return cls(equipment_type, int(row[0]), Stats(
            float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])
        ))
    
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Equipment{type=%s,id=%s,%s}" % (self.equipment_type.value, self.id, self.stats)

class Player(object):
    def __init__(self, player_class, height, weapon, boots, helmet, gloves, armor):
        """Returns a Player object with the given height and equipments

        Parameters
        ----------
        player_class : PlayerClass
            Type of player
        height : float
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
        self.s_player_stats = None
        self.s_attack_mod = None
        self.s_defense_mod = None
        self.s_attack = None
        self.s_defense = None
        self.s_fitness = None
    
    def player_stats(self):
        # Player Stats is an object, no need to add is not None to condition
        if self.s_player_stats:
            return self.s_player_stats

        # Accumulate item stats
        total_item_stats = Stats(0, 0, 0, 0, 0)
        for item in [self.weapon, self.boots, self.helmet, self.gloves, self.armor]:
            total_item_stats.add_stats(item.stats)
        
        # Calculate player stats
        self.s_player_stats = Stats(
            100 * math.tanh(0.01 * total_item_stats.strength),
            math.tanh(0.01 * total_item_stats.agility),
            0.6 * math.tanh(0.01 * total_item_stats.expertise),
            math.tanh(0.01 * total_item_stats.resistance),
            100 * math.tanh(0.01 * total_item_stats.life))
        
        return self.s_player_stats
    
    def height_modifiers(self):
        # Check for None as modifiers could be 0
        if self.s_attack_mod is not None and self.s_defense_mod is not None:
            return (self.s_attack_mod, self.s_defense_mod)
    
        # Calculate height modifiers
        self.s_attack_mod = 0.7 - math.pow(3 * self.height - 5, 4) + math.pow(3 * self.height - 5, 2) + self.height / 4
        self.s_defense_mod = 1.9 + math.pow(2.5 * self.height - 4.16, 4) - math.pow(2.5 * self.height - 4.16, 2) - 3 * self.height / 10

        return (self.s_attack_mod, self.s_defense_mod)
    
    def final_stats(self):
        # Check for None as final stats could be 0
        if self.s_attack is not None and self.s_defense is not None:
            return (self.s_attack, self.s_defense)
    
        # Set player stats if not done before
        self.player_stats()
        # Set height modifiers if not done before
        self.height_modifiers()

        self.s_attack = (self.s_player_stats.agility + self.s_player_stats.expertise) * self.s_player_stats.strength * self.s_attack_mod
        self.s_defense = (self.s_player_stats.resistance + self.s_player_stats.expertise) * self.s_player_stats.life * self.s_defense_mod

        return (self.s_attack, self.s_defense)
    
    def fitness(self):
        # Check for None as fitness could be 0
        if self.s_fitness is not None:
            return self.s_fitness

        # Set final stats if not done before
        self.final_stats()

        self.s_fitness = self.player_class(self.s_attack, self.s_defense)

        return self.s_fitness

    def __lt__(self, other):
        # Set self and other fitness if not done before
        self.fitness()
        other.fitness()

        return self.s_fitness - other.s_fitness

