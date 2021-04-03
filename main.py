import time
import json
import sys
import signal
import math

import utils
import player as ply
import mutations as mut
import selector as sel
import crossovers as cros
import stoppers as stp
import genetic as gen
import matplotlib.pyplot as plt

# Define signal handler for Ctrl+C for ordered interrupt
def signal_handler(sig, frame):
    if algo and start_time:
        print(f'\nAlgorithm Run Interrupted by Ctrl+C \t\t ⏱  {round(time.time() - start_time, 6)} seconds\n----------------------------------------\n')
        print(f'Best fit so far: {algo.best_fit}')
    print('\nExiting by SIGINT...')
    sys.exit(2)

signal.signal(signal.SIGINT, signal_handler)

algo = None

# Parse each TSV to get List of possible value for each equipment type
weapon_list = utils.read_equipment_tsv("dataset/armas.tsv", ply.EquipmentType.Weapon, 1000000)
boots_list = utils.read_equipment_tsv("dataset/botas.tsv", ply.EquipmentType.Boots, 1000000)
helmet_list = utils.read_equipment_tsv("dataset/cascos.tsv", ply.EquipmentType.Helmet, 1000000)
gloves_list = utils.read_equipment_tsv("dataset/guantes.tsv", ply.EquipmentType.Gloves, 1000000)
armor_list = utils.read_equipment_tsv("dataset/pecheras.tsv", ply.EquipmentType.Armor, 1000000)



# Read params from config


# Population count
N = 100

# Child count
K = 30
i = 0
crossover_dic = {
    'one_point': cros.Crossover.one_point,
    'two_points': cros.Crossover.two_points,
    'ring': cros.Crossover.ring,
    'uniform': cros.Crossover.uniform}

mutation_dic = {
    'simple_gen': mut.SimpleGen,
    'multi_limited': mut.MultiLimited,
    'multi_uniform': mut.MultiUniform,
    'full': mut.Full}

selector_dic = {
    'elite': sel.EliteSelector,
    'roulette': sel.RouletteSelector,
    'universal': sel.UniversalSelector,
    'ranking': sel.RankingSelector,
    'boltzmann': sel.BoltzmannSelector,
    'deterministic_tournament': sel.DeterministicTournamentSelector,
    'probabilistic_tournament': sel.ProbabilisticTournamentSelector}

implementation_dic = {
    'fill-all': True,
    'fill-parent': False}

stopper_instance_dic = {
    'stopper_time_on': stp.TimeStopper,
    'stopper_generation_count_on': stp.GenerationCountStopper,
    'stopper_diversity_on': stp.DiversityStopper,
    'stopper_acceptable_on': stp.AcceptableSolutionStopper,
    'stopper_structural_on': stp.StructuralStopper,
    'stopper_content_on': stp.ContentStopper}

stopper_params_dic = {
    'stopper_time_on': ['stop_time_sec'],
    'stopper_generation_count_on': ['stop_generation_count'],
    'stopper_diversity_on': ['stop_diversity_proportion'],
    'stopper_acceptable_on': ['stop_acceptable_fitness'],
    'stopper_structural_on': ['stop_structural_gen_count', 'stop_structural_proportion'],
    'stopper_content_on': ['stop_content_gen_count']}

# Read configurations from file
with open("config.json") as file:
    config = json.load(file)


stopper_list = []
for name in stopper_instance_dic:
    stopper_boolean = utils.read_config_param(
        config, name, lambda el : bool(el), lambda el : False)
    if stopper_boolean:
        param_list = []
        for param_name in stopper_params_dic[name]:
            param_list.append(utils.read_config_param(
                config, param_name, lambda el : float(el), lambda el : False))
        if not stopper_instance_dic[name].is_param_list_valid(param_list):
            utils.invalid_param(stopper_params_dic[name])
        stopper_list.append(stopper_instance_dic[name].new_from_param_list(param_list))
if not stopper_list:
    print(f'Error in config. Some stopper must be turned on!')
    sys.exit(1)

# Fitness delta configuration
ply.Player.set_fitness_delta(1e-4)

# Random seed configuration
#utils.set_random_seed("SUPER_RANDOM_SEED")


for crossover_fun_name in crossover_dic:
    for implementation_name in implementation_dic:
        for selector_A in range(0, 100, 5):
            selector_A = selector_A / 100
            for selector_B in range(0, 100, 5):
                selector_B = selector_B / 100
                for mutation_probability in range(1, 9, 1):
                    mutation_probability = mutation_probability / 10

                    # Selector functions
                    for selector_m1_name in selector_dic:
                        for selector_m2_name in selector_dic:
                            for selector_m3_name in selector_dic:
                                for selector_m4_name in selector_dic:

                                    for mutation_instance_name in mutation_dic:

                                        # If mutation is multi_limited, read M value
                                        if mutation_instance_name == 'multi_limited':
                                            limited_multigen_m = 6

                                        # Check parameters for parent selectors
                                        selector_parent_list = [selector_m1_name, selector_m2_name]
                                        (any_par_det_tournament, any_par_prob_tournament, any_par_boltzmann) = (False, False, False)

                                        # If any selector is deterministic_tournament, read M value
                                        if any(name == 'deterministic_tournament' for name in selector_parent_list):
                                            any_par_det_tournament = True
                                            # from 1 to N included
                                            selector_par_det_m = 3


                                        # If any selector is probabilistic_tournament, read Threshold value
                                        if any(name == 'probabilistic_tournament' for name in selector_parent_list):
                                            any_par_prob_tournament = True
                                            # from 0.5 to 1 included
                                            selector_par_prob_th = 0.7


                                        # If any selector is boltzmann, read T0 and Tc
                                        if any(name == 'boltzmann' for name in selector_parent_list):
                                            any_par_boltzmann = True
                                            # bigger than 0
                                            selector_par_boltzmann_t0 = 10.0
                                            # bigger than 0, smaller than selector_par_boltzmann_t0
                                            selector_par_boltzmann_tc = 1.0
                                            # bigger than 0
                                            selector_par_boltzmann_k = 0.2

                                        # Check whether to shuffle or not parent output
                                        selector_par_shuffle = False

                                        # Check parameters for replacement selectors
                                        selector_replace_list = [selector_m3_name, selector_m4_name]
                                        (any_rep_det_tournament, any_rep_prob_tournament, any_rep_boltzmann) = (False, False, False)


                                        # If any selector is deterministic_tournament, read M value
                                        if any(name == 'deterministic_tournament' for name in selector_replace_list):
                                            any_rep_det_tournament = True
                                            # from 1 to N included
                                            selector_rep_det_m = 3


                                        # If any selector is probabilistic_tournament, read Threshold value
                                        if any(name == 'probabilistic_tournament' for name in selector_replace_list):
                                            any_rep_prob_tournament = True
                                            # from 0.5 to 1 included
                                            selector_rep_prob_th = 0.8


                                        # If any selector is boltzmann, read T0 and Tc
                                        if any(name == 'boltzmann' for name in selector_replace_list):
                                            any_rep_boltzmann = True
                                            # bigger than 0
                                            selector_rep_boltzmann_t0 = 10.0
                                            # bigger than 0, smaller than selector_par_boltzmann_t0
                                            selector_rep_boltzmann_tc = 1.0
                                            # bigger than 0
                                            selector_rep_boltzmann_k = 0.2


                                        # Create Generation 0
                                        base_generation = utils.generate_players(
                                            N, ply.PlayerClass.Guerrero,
                                            weapon_list, boots_list, helmet_list, gloves_list, armor_list)

                                        # print("Generation 0\n", base_generation)

                                        selector_list = []
                                        for sel_name in selector_parent_list:
                                            if sel_name == 'deterministic_tournament':
                                                selector = selector_dic[sel_name](selector_par_det_m)
                                            elif sel_name == 'probabilistic_tournament':
                                                selector = selector_dic[sel_name](selector_par_prob_th)
                                            elif sel_name == 'boltzmann':
                                                selector = selector_dic[sel_name](selector_par_boltzmann_t0, selector_par_boltzmann_tc, selector_par_boltzmann_k)
                                            else:
                                                selector = selector_dic[sel_name]()
                                            selector_list.append(selector)

                                        for sel_name in selector_replace_list:
                                            if sel_name == 'deterministic_tournament':
                                                selector = selector_dic[sel_name](selector_rep_det_m)
                                            elif sel_name == 'probabilistic_tournament':
                                                selector = selector_dic[sel_name](selector_rep_prob_th)
                                            elif sel_name == 'boltzmann':
                                                selector = selector_dic[sel_name](selector_rep_boltzmann_t0, selector_rep_boltzmann_tc, selector_rep_boltzmann_k)
                                            else:
                                                selector = selector_dic[sel_name]()
                                            selector_list.append(selector)

                                        parent_selectors = sel.CombinedSelector(
                                            selector_list[0],
                                            selector_list[1],
                                            selector_A,
                                            selector_par_shuffle)
                                        replace_selectors = sel.CombinedSelector(
                                            selector_list[2],
                                            selector_list[3],
                                            selector_B)
                                        if mutation_instance_name == 'multi_limited':
                                            mutation = mutation_dic[mutation_instance_name](
                                                mutation_probability, limited_multigen_m,
                                                weapon_list, boots_list, helmet_list, gloves_list, armor_list
                                            )
                                        else:
                                            mutation = mutation_dic[mutation_instance_name](
                                                mutation_probability,
                                                weapon_list, boots_list, helmet_list, gloves_list, armor_list
                                            )
                                        # Stopper List already built in stopper_list

                                        # Create algorithm function configuration
                                        algo_fun_config = gen.AlgorithmFunctionsConfig(
                                            parent_selectors,
                                            replace_selectors,
                                            crossover_dic[crossover_fun_name],
                                            mutation,
                                            stopper_list
                                        )

                                        start_time = time.time()

                                        # Create algorithm instance
                                        algo = gen.GeneticAlgorithm(
                                            base_generation, K, algo_fun_config,
                                            implementation_dic[implementation_name])

                                        while not algo.is_algorithm_over():
                                            curr_gen = algo.iterate()

                                        i = i + 1
                                        if algo.best_fit.fitness() > 25.0:
                                            # Print config params
                                            print(f'---------------------------------------- \n')
                                            print(f'\tIteration Number:\t{i}')
                                            print(f'---------------------------------------- \n'
                                                  f'Run parameters\n'
                                                  f'\tPlayer class:\tguerrero\n'
                                                  f'\tMax. Rows:\t1000000\n'
                                                  f'\tN:\t\t{N}\n'
                                                  f'\tK:\t\t{K}\n'
                                                  f'\tCrossover:\t{crossover_fun_name}\n'
                                                  f'\tMutation:\t{mutation_instance_name}\n'
                                                  f'\tMutation prob:\t{mutation_probability}'
                                                  )
                                            if mutation_instance_name == 'multi_limited': print(
                                                f'\tMutation M:\t{limited_multigen_m}')
                                            print(f'\n\tSelector A:\t{selector_A}\n'
                                                  f'\tSelector m1:\t{selector_m1_name}\n'
                                                  f'\tSelector m2:\t{selector_m2_name}\n'
                                                  f'\tShuffle:\t{selector_par_shuffle}'
                                                  )
                                            if any_par_det_tournament: print(f'\tDet. Tour. M:\t{selector_par_det_m}')
                                            if any_par_prob_tournament: print(
                                                f'\tProb. Tour. Th:\t{selector_par_prob_th}')
                                            if any_par_boltzmann:
                                                print(f'\tBoltzmann T0:\t{selector_par_boltzmann_t0}\n'
                                                      f'\tBoltzmann TC:\t{selector_par_boltzmann_tc}\n'
                                                      f'\tBoltzmann K:\t{selector_par_boltzmann_k}'
                                                      )
                                            print(f'\n\tSelector B:\t{selector_B}\n'
                                                  f'\tSelector m3:\t{selector_m3_name}\n'
                                                  f'\tSelector m4:\t{selector_m4_name}'
                                                  )
                                            if any_rep_det_tournament: print(f'\tDet. Tour. M:\t{selector_rep_det_m}')
                                            if any_rep_prob_tournament: print(
                                                f'\tProb. Tour. Th:\t{selector_rep_prob_th}')
                                            if any_rep_boltzmann:
                                                print(f'\tBoltzmann T0:\t{selector_rep_boltzmann_t0}\n'
                                                      f'\tBoltzmann TC:\t{selector_rep_boltzmann_tc}\n'
                                                      f'\tBoltzmann K:\t{selector_rep_boltzmann_k}'
                                                      )
                                            print(f'\n\tImplementation:\t{implementation_name}')
                                            for stopper in stopper_list:
                                                print(f'\tStopper:\t{stopper}')
                                            print('----------------------------------------')

                                            print(f'Algorithm Run Completed by {algo.current_stopper} \t ⏱  {round(time.time() - start_time, 6)} seconds\n----------------------------------------\n')

                                            # Print result
                                            print(f'Best fit: {algo.best_fit}')

