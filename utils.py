import csv, itertools
import random
import sys
import player as ply
import time
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

(min_height, max_height) = (1.3, 2.0)

def set_random_seed(seed):
    random.seed(seed)

def invalid_param(param_name):
    print(f'Error in config. Invalid or missing {param_name}!')
    sys.exit(1)

def read_config_param(config, param_name, converter_fun, invalid_fun):
    if param_name in config:
        param = converter_fun(config[param_name])
        if not invalid_fun(param):
            return param
    invalid_param(param_name)

def read_equipment_tsv(filename, equipment_type, max_rows):
    with open(filename) as file:
        tsv_reader = csv.reader(file, delimiter="\t")
        next(tsv_reader) # Skip header column
        return [ply.Equipment.new_from_row(equipment_type, row) for row in itertools.islice(tsv_reader, max_rows)]

def generate_players(count, player_class, weapon_list, boots_list, helmet_list, gloves_list, armor_list):
    players = []
    for i in range(count):
        player = ply.Player(
            player_class,
            random.uniform(min_height, max_height), 
            weapon_list[random.randint(0, len(weapon_list) - 1)],
            boots_list[random.randint(0, len(boots_list) - 1)], 
            helmet_list[random.randint(0, len(helmet_list) - 1)], 
            gloves_list[random.randint(0, len(gloves_list) - 1)], 
            armor_list[random.randint(0, len(armor_list) - 1)])
        players.append(player)
    
    return players

def print_algorithm_stats(algo):
    print(f'Gen {algo.generation_count}\t'
          f'Best fitness {round(algo.best_fit.fitness(), ply.Player.FIT_DEC_COUNT)}\t'
          f'Worst fitness {round(algo.worst_fit.fitness(), ply.Player.FIT_DEC_COUNT)}\t'
          f'Avg fitness {round(algo.avg_fitness, ply.Player.FIT_DEC_COUNT)}\n'
          f'Diversity {round(algo.diversity * 100, ply.Player.FIT_DEC_COUNT)}%  '
          f'Generation Changes {algo.generation_changes}\n')

def plot_stats(algo, axi, interval=0.3):
    axi[0].scatter(algo.generation_count, algo.best_fit.fitness(), c='red')
    axi[0].scatter(algo.generation_count, algo.worst_fit.fitness(), c='gold')
    axi[0].scatter(algo.generation_count, algo.avg_fitness, c='darkorange')
    axi[1].scatter(algo.generation_count, algo.diversity, c='green')
    # plt.pause(interval)
    my_plt_pause(interval)

def my_plt_pause(interval):
    manager = plt._pylab_helpers.Gcf.get_active()
    if manager is not None:
        canvas = manager.canvas
        if canvas.figure.stale:
            canvas.draw_idle()        
        canvas.start_event_loop(interval)
    else:
        time.sleep(interval)

# x, y = [], []
# def animate(value, gen):
#     x.append(value)
#     y.append(gen)
#     plt.plot(x,y)
# ani = FuncAnimation(plt.gcf(), animate, interval=1000)
