import enum
import math

# Possible player classes
# Use eg: player.PlayerClass.Arquero.fitness(10, 20)
class PlayerClass(enum.Enum):
    class ClassType(object):
        def __init__(self, attack_mult, defense_mult, emoji):
            self.attack_mult = attack_mult
            self.defense_mult = defense_mult
            self.emoji = emoji
        
        def fitness(self, attack, defense):
            return self.attack_mult * attack + self.defense_mult * defense
        
    Guerrero = ClassType(0.6, 0.6, "๐ก๏ธ ")
    Arquero = ClassType(0.9, 0.1, "๐น ")
    Defensor = ClassType(0.3, 0.8, "๐ก๏ธ ")
    Infiltrado = ClassType(0.8, 0.3, "๐ต ")

    def fitness(self, attack, defense):
        return self.value.fitness(attack, defense)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "%s(%s)" % (self.name, self.value.emoji)

class EquipmentType(enum.Enum):
    Weapon = "๐ฅ "
    Boots = "๐ฅพ "
    Helmet = "โ๏ธ  "
    Gloves = "๐งค "
    Armor = "๐ฅ "

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "%s(%s)" % (self.name, self.value)

    # Define hash and eq methods to allow comparation in equipment hash and eq
    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not (self == other)

class Stats(object):
    PRINT_DEC = 3

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
        return "Stats(str=%s,ag=%s,exp=%s,res=%s,lif=%s)" % (round(self.strength, self.PRINT_DEC), 
            round(self.agility, self.PRINT_DEC), round(self.expertise, self.PRINT_DEC), 
            round(self.resistance, self.PRINT_DEC), round(self.life, self.PRINT_DEC))

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
        return "Equip{%s,id=%s,%s}" % (self.equipment_type.value, self.id, self.stats)

    # Define hash and eq methods to allow comparation in player hash and eq
    def __hash__(self):
        return hash(self.id) + 31 * hash(self.equipment_type)

    def __eq__(self, other):
        if self.equipment_type != other.equipment_type:
            return False
        return self.id == other.id

    def __ne__(self, other):
        return not (self == other)

class Player(object):

    n_genes = 6
    HEIGHT_POS, WEAPON_POS, BOOTS_POS = 0, 1, 2
    HELMET_POS, GLOVES_POS, ARMOR_POS = 3, 4, 5

    FIT_ABS_TOL = 1e-4
    FIT_DEC_COUNT = math.ceil(abs(math.log10(FIT_ABS_TOL)))

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

        # We assume each equipment_type will be valid, gaining performance
        # if weapon.equipment_type != EquipmentType.Weapon:
        #     raise ValueError("Not a weapon!")
        # if boots.equipment_type != EquipmentType.Boots:
        #     raise ValueError("Not boots!")
        # if helmet.equipment_type != EquipmentType.Helmet:
        #     raise ValueError("Not a helmet!")
        # if gloves.equipment_type != EquipmentType.Gloves:
        #     raise ValueError("Not gloves!")
        # if armor.equipment_type != EquipmentType.Armor:
        #     raise ValueError("Not an armor!")

        self.weapon = weapon
        self.boots = boots
        self.helmet = helmet
        self.gloves = gloves
        self.armor = armor

        # Initialize stat saved values to None, will be calculated and stored on demand
        self.reset_saved_values()

    @classmethod
    def set_fitness_delta(cls, delta):
        cls.FIT_ABS_TOL = delta
        cls.FIT_DEC_COUNT = math.ceil(abs(math.log10(delta)))

    def reset_saved_values(self):
        self.s_player_stats = None
        self.s_attack_mod = None
        self.s_defense_mod = None
        self.s_attack = None
        self.s_defense = None
        self.s_fitness = None
    
    @classmethod
    def new_from_array(cls, player_class, gene_array):
        """Returns a Player object with the given genes

        Parameters
        ----------
        player_class : PlayerClass
            Type of player
        gene_array : list of genes
            Array of genes. Expected order is [height, weapon, boots, helmet, gloves, armor]
        """
        # height, weapon, boots, helmet, gloves, armor):
        return cls(
            player_class, 
            gene_array[cls.HEIGHT_POS], 
            gene_array[cls.WEAPON_POS], 
            gene_array[cls.BOOTS_POS], 
            gene_array[cls.HELMET_POS], 
            gene_array[cls.GLOVES_POS], 
            gene_array[cls.ARMOR_POS])

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

        self.s_fitness = self.player_class.fitness(self.s_attack, self.s_defense)

        return self.s_fitness

    def __lt__(self, other):
        # Set self and other fitness if not done before
        self.fitness()
        other.fitness()
        return self.s_fitness < other.s_fitness
        
    def genes(self):
        genes = [None] * self.n_genes
        genes[self.HEIGHT_POS] = self.height
        genes[self.WEAPON_POS] = self.weapon
        genes[self.BOOTS_POS] = self.boots
        genes[self.HELMET_POS] = self.helmet
        genes[self.GLOVES_POS] = self.gloves
        genes[self.ARMOR_POS] = self.armor
        return genes

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Player(%s,height=%s meters\nfitness=%s(attack=%s,defense=%s,ATM=%s,DEM=%s)\n%s\n%s\n%s\n%s\n%s\n)" % (self.player_class, 
                round(self.height, self.FIT_DEC_COUNT), round(self.fitness(), self.FIT_DEC_COUNT), 
                round(self.s_attack, self.FIT_DEC_COUNT), round(self.s_defense, self.FIT_DEC_COUNT),
                round(self.s_attack_mod, self.FIT_DEC_COUNT), round(self.s_defense_mod, self.FIT_DEC_COUNT),
                self.weapon, self.boots, self.helmet, self.gloves, self.armor)

    # Define hash and eq methods to allow key usage --> Diversity + Population change (StructuralStopper)
    # Two players are equal if their fitness is close enough
    def __hash__(self):
        return hash(round(self.fitness(), self.FIT_DEC_COUNT))

    def __eq__(self, other):
        return math.isclose(self.fitness(), other.fitness(), abs_tol=self.FIT_ABS_TOL)

    def __ne__(self, other):
        return not (self == other)