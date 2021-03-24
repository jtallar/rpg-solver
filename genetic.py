import random

(min_height, max_height) = (1.3, 2.0)

class GeneticAlgorithm(object):
    def __init__(self, count):
        self.count = count

# TODO: Ver si este metodo hay que meterlo adentro de la clase
def generate_players(count, player_class, weapon_list, boots_list, helmet_list, gloves_list, armor_list):
    players = []
    for i in range(count):
        player = obj.Player(
            player_class,
            random.uniform(min_height, max_height), 
            weapon_list[random.randint(0, len(weapon_list) - 1)],
            boots_list[random.randint(0, len(boots_list) - 1)], 
            helmet_list[random.randint(0, len(helmet_list) - 1)], 
            gloves_list[random.randint(0, len(gloves_list) - 1)], 
            armor_list[random.randint(0, len(armor_list) - 1)])
        players.append(player)
    
    return players