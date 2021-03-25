import time
import json
import sys
import signal

import utils
import player as obj
import mutations as mut
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
weapon_list = utils.read_equipment_tsv(config["armas_file"], obj.EquipmentType.Weapon, max_rows)
boots_list = utils.read_equipment_tsv(config["botas_file"], obj.EquipmentType.Boots, max_rows)
helmet_list = utils.read_equipment_tsv(config["cascos_file"], obj.EquipmentType.Helmet, max_rows)
gloves_list = utils.read_equipment_tsv(config["guantes_file"], obj.EquipmentType.Gloves, max_rows)
armor_list = utils.read_equipment_tsv(config["pecheras_file"], obj.EquipmentType.Armor, max_rows)

end_time = time.time()
print(f'TSV Parsing \t\t ⏱  {round(end_time - start_time, 6)} seconds')
start_time = end_time

base_generation = utils.generate_players(
    10, obj.PlayerClass.Arquero, 
    weapon_list, boots_list, helmet_list, gloves_list, armor_list)

print(base_generation)