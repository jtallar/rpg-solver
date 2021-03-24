import enum

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

class Equipment(object):
    def __init__(self, equipment_type, id, strength, agility, expertise, resistance, life):
        """Returns an Equipment object with the given stats

        Parameters
        ----------
        equipment_type : EquipmentType
            Type of equipment
        id : int
            Equipment id
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

        self.equipment_type = equipment_type
        self.id = id
        self.strength = strength
        self.agility = agility
        self.expertise = expertise
        self.resistance = resistance
        self.life = life

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
