import player as obj
import time
import json
import sys
import signal
import csv, itertools
import random
import functions as fn

import selectors as sel

# Define signal handler for Ctrl+C for ordered interrupt
def signal_handler(sig, frame):
    # TODO: Change this to corresponding function calls
    # if algo and not algo.winner_node and start_time:
    #     print(f'\nAlgorithm Run Interrupted \t\t ⏱  {round(time.time() - start_time, 6)} seconds\n----------------------------------------\n')
    #     print("\t❌  Failure by Ctrl+C! No solution found with those params. ❌ ")
    #     print(f'\nExpanded nodes: {algo.expanded_count}')
    print('\nExiting by SIGINT...')
    sys.exit(2)

signal.signal(signal.SIGINT, signal_handler)

def read_equipment_tsv(filename, equipment_type, max_rows):
    with open(filename) as file:
        tsv_reader = csv.reader(file, delimiter="\t")
        next(tsv_reader) # Skip header column
        return [obj.Equipment.new_from_row(equipment_type, row) for row in itertools.islice(tsv_reader, max_rows)]

start_time = time.time()

# Read configurations from file
with open("config.json") as file:
    config = json.load(file)

# Number of lines per file limited by max_rows config
max_rows = int(config["max_rows_tsv"])
if max_rows <= 0:
    print("Invalid max rows!")
    sys.exit(1)

# Parse each TSV to get List of possible value for each equipment type
weapon_list = read_equipment_tsv(config["armas_file"], obj.EquipmentType.Weapon, max_rows)
boots_list = read_equipment_tsv(config["botas_file"], obj.EquipmentType.Boots, max_rows)
helmet_list = read_equipment_tsv(config["cascos_file"], obj.EquipmentType.Helmet, max_rows)
gloves_list = read_equipment_tsv(config["guantes_file"], obj.EquipmentType.Gloves, max_rows)
armor_list = read_equipment_tsv(config["pecheras_file"], obj.EquipmentType.Armor, max_rows)

end_time = time.time()
print(f'TSV Parsing \t\t ⏱  {round(end_time - start_time, 6)} seconds')
start_time = end_time

Weapon = weapon_list[random.randint(0, len(weapon_list) - 1)]
Boots = boots_list[random.randint(0, len(boots_list) - 1)]
Helmet = helmet_list[random.randint(0, len(helmet_list) - 1)]
Gloves = gloves_list[random.randint(0, len(gloves_list) - 1)]
Armor = armor_list[random.randint(0, len(armor_list) - 1)]

# print(Weapon, Boots, Helmet, Gloves, Armor)

player = obj.Player(obj.PlayerClass.Arquero, 1.3, Weapon, Boots, Helmet, Gloves, Armor)
player2 = obj.Player(obj.PlayerClass.Arquero, 2.0, Weapon, Boots, Helmet, Gloves, Armor)
arr = [player, player2]
for index, el in enumerate(arr):
    el.fitness_prime = 12 - el.fitness()
# print(player.fitness(), player2.fitness())

# print(sel.Selector.probabilistic_tournament_selector(2, arr, 0.75))

# player.player_stats()
# print(player.fitness(), time.time() - start_time)
start_time = time.time()
# print(player.fitness(), time.time() - start_time)
# print(player.genes(), '\n')
# print(fn.SimpleGen(0.8, weapon_list, boots_list, helmet_list, gloves_list, armor_list).mutate(player).genes())
# print(fn.MultiLimited(0.8, weapon_list, boots_list, helmet_list, gloves_list, armor_list).mutate(player).genes())
# print(fn.MultiUniform(0.5, weapon_list, boots_list, helmet_list, gloves_list, armor_list).mutate(player).genes())
# print(fn.Full(1, weapon_list, boots_list, helmet_list, gloves_list, armor_list).mutate(player).genes())