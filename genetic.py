import random

(min_height, max_height) = (1.3, 2.0)

class GeneticAlgorithmFunctions(object):
    def __init__(self, parent_selectors, replace_selectors, crossover_function, mutation_instance, stop_function):
        """Returns a Genetic Algorithm Functions instance
        
        Parameters
        ----------
        parent_selectors : CombinedSelector
            Combined selector to use when selecting K parents
        replace_selectors : CombinedSelector
            Combined selector to use when selecting N players for next gen
        crossover_function : function

        mutation_instance : Mutation

        stop_function : function
        """

        self.parent_selectors = parent_selectors
        self.replace_selectors = replace_selectors
        self.crossover_function = crossover_function
        self.mutation_instance = mutation_instance
        self.stop_function = stop_function


class GeneticAlgorithm(object):
    def __init__(self, base_gen_collection, son_count, function_config, fill_all):
        """Returns a Genetic Algorithm instance
        
        Parameters
        ----------
        base_gen_collection : list
            Generation 0 of players. N = len(base_gen_collection)
        son_count : int
            Number of childs to generate in each iteration. K = son_count
        function_config : GeneticAlgorithmFunctions
            Object with desired functions for selectors, crossover, mutation and stopping
        fill_all : boolean
            If true, use fill_all. If false, use fill_parent
        """

        self.base_gen_collection = base_gen_collection
        self.son_count = son_count
        self.function_config = function_config
        self.fill_all = fill_all

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