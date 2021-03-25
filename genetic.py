import time

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
            Function used to perform crossover between 2 parents, generating 2 childs
        mutation_instance : Mutation
            Instance used to perform mutations on a player
        stop_function : function
            Function used to determine when to stop iteration
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

        self.player_collection = base_gen_collection
        self.N = len(base_gen_collection)
        self.K = son_count
        self.function_config = function_config
        self.fill_all = fill_all
        self.start_time = time.time()
        self.generation_count = 0
    
    def is_algorithm_over(self):
        pass

    def iterate(self):
        # Select K parents from player_collection

        # Cross parents, generating K childs

        # Mutate each child

        # Select N from N (actual) + K (childs) to save new generation
