import time
import json
import sys
import signal

import utils
import player as ply
import mutations as mut
import selectors as sel
import crossovers as cros
import stoppers as stp

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

# TODO: Ver si los nombres de las config tienen que ser si o si A, B, method1, etc o si podemos definirlas en el README
# Read configurations from file
with open("config.json") as file:
    config = json.load(file)

# Read params from config
# Number of lines per file limited by max_rows config
max_rows = utils.read_config_param(
    config, "max_rows_tsv", lambda el : int(el), lambda el : el <= 0)
# Player class
player_class_dic = {
    'guerrero': ply.PlayerClass.Guerrero, 
    'arquero': ply.PlayerClass.Arquero, 
    'defensor': ply.PlayerClass.Defensor, 
    'infiltrado': ply.PlayerClass.Infiltrado}
player_class_name = utils.read_config_param(
    config, "player_class", lambda el : el, lambda el : el not in player_class_dic)
# Population count
N = utils.read_config_param(
    config, "N", lambda el : int(el), lambda el : el <= 0)
# Child count
K = utils.read_config_param(
    config, "K", lambda el : int(el), lambda el : el <= 0)
# Crossover function
crossover_dic = {
    'one_point': cros.Crossover.one_point, 
    'two_points': cros.Crossover.two_points, 
    'ring': cros.Crossover.ring, 
    'uniform': cros.Crossover.uniform}
crossover_fun_name = utils.read_config_param(
    config, "crossover", lambda el : el, lambda el : el not in crossover_dic)
# Mutation function
mutation_dic = {
    'simple_gen': mut.SimpleGen, 
    'multi_limited': mut.MultiLimited, 
    'multi_uniform': mut.MultiUniform, 
    'full': mut.Full}
mutation_instance_name = utils.read_config_param(
    config, "mutation", lambda el : el, lambda el : el not in mutation_dic)
# Mutation probability
mutation_probability = utils.read_config_param(
    config, "mutation_probability", lambda el : float(el), lambda el : el < 0 or el > 1)
# If mutation is multi_limited, read M value
if mutation_instance_name == 'multi_limited':
    limited_multigen_m = utils.read_config_param(
        config, "limited_multigen_m", lambda el : int(el), lambda el : el < 1 or el > ply.Player.n_genes)
# Selector functions
selector_dic = {
    'elite': sel.Selector.elite_selector, 
    'roulette': sel.Selector.roulette_selector, 
    'universal': sel.Selector.universal_selector, 
    'ranking': sel.Selector.ranking_selector, 
    'boltzmann': sel.Selector.boltzmann_selector, 
    'deterministic_tournament': sel.Selector.deterministic_tournament_selector, 
    'probabilistic_tournament': sel.Selector.probabilistic_tournament_selector}
selector_m1_name = utils.read_config_param(
    config, "selector_method_1", lambda el : el, lambda el : el not in selector_dic)
selector_m2_name = utils.read_config_param(
    config, "selector_method_2", lambda el : el, lambda el : el not in selector_dic)
selector_m3_name = utils.read_config_param(
    config, "selector_method_3", lambda el : el, lambda el : el not in selector_dic)
selector_m4_name = utils.read_config_param(
    config, "selector_method_4", lambda el : el, lambda el : el not in selector_dic)
# Selector A and B percentages
selector_A = utils.read_config_param(
    config, "A", lambda el : float(el), lambda el : el < 0 or el > 1)
selector_B = utils.read_config_param(
    config, "B", lambda el : float(el), lambda el : el < 0 or el > 1)
# Implementation method
implementation_dic = {
    'fill-all': True, 
    'fill-parent': False}
implementation_name = utils.read_config_param(
    config, "implementation", lambda el : el, lambda el : el not in implementation_dic)
# Stopper function
stopper_dic = {
    'time': stp.TimeStopper, 
    'generation_count': stp.GenerationCountStopper, 
    'acceptable_solution': stp.AcceptableSolutionStopper, 
    'structural': stp.StructuralStopper,
    'content': stp.ContentStopper}
stopper_instance_name = utils.read_config_param(
    config, "stopper", lambda el : el, lambda el : el not in stopper_dic)
# Stopper n - first param
stopper_n = utils.read_config_param(
    config, "stopper_n", lambda el : float(el), lambda el : el <= 0)
# If stopper is structural, read r value
if stopper_instance_name == 'structural':
    stopper_r = utils.read_config_param(
        config, "stopper_r", lambda el : float(el), lambda el : el <= 0 or el > 1)

end_time = time.time()
print(f'Load Configuration \t ⏱  {round(end_time - start_time, 6)} seconds')
start_time = end_time

# Parse each TSV to get List of possible value for each equipment type
weapon_list = utils.read_equipment_tsv(config["armas_file"], ply.EquipmentType.Weapon, max_rows)
boots_list = utils.read_equipment_tsv(config["botas_file"], ply.EquipmentType.Boots, max_rows)
helmet_list = utils.read_equipment_tsv(config["cascos_file"], ply.EquipmentType.Helmet, max_rows)
gloves_list = utils.read_equipment_tsv(config["guantes_file"], ply.EquipmentType.Gloves, max_rows)
armor_list = utils.read_equipment_tsv(config["pecheras_file"], ply.EquipmentType.Armor, max_rows)

end_time = time.time()
print(f'TSV Parsing \t\t ⏱  {round(end_time - start_time, 6)} seconds')
start_time = end_time

base_generation = utils.generate_players(
    N, player_class_dic[player_class_name], 
    weapon_list, boots_list, helmet_list, gloves_list, armor_list)

print(base_generation)