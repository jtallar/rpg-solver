import csv, itertools
import random
import player as obj

(min_height, max_height) = (1.3, 2.0)

def read_equipment_tsv(filename, equipment_type, max_rows):
    with open(filename) as file:
        tsv_reader = csv.reader(file, delimiter="\t")
        next(tsv_reader) # Skip header column
        return [obj.Equipment.new_from_row(equipment_type, row) for row in itertools.islice(tsv_reader, max_rows)]

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