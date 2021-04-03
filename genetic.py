import time

class AlgorithmFunctionsConfig(object):
    def __init__(self, parent_selectors, replace_selectors, crossover_function, mutation_instance, stop_instance_list):
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
        stop_instance_list : List of Stopper
            List of instances used to determine when to stop iteration
        """

        self.parent_selectors = parent_selectors
        self.replace_selectors = replace_selectors
        self.crossover_function = crossover_function
        self.mutation_instance = mutation_instance
        self.stop_instance_list = stop_instance_list


class GeneticAlgorithm(object):
    def __init__(self, base_gen_collection, son_count, function_config, fill_all):
        """Returns a Genetic Algorithm instance
        
        Parameters
        ----------
        base_gen_collection : list
            Generation 0 of players. N = len(base_gen_collection)
        son_count : int
            Number of childs to generate in each iteration. K = son_count
        function_config : AlgorithmFunctionsConfig
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
        self.previous_generation = {}
        self.update_algo_stats()
        self.current_stopper = None

    def update_algo_stats(self):
        generation_changes = 0
        current_generation = {}

        sum_fitness = 0
        worst_fit = best_fit = self.player_collection[0]
        for player in self.player_collection:
            # Update best fit & worst fit
            if player > best_fit: best_fit = player
            if player < worst_fit: worst_fit = player
            # Accumulate fitness
            sum_fitness += player.fitness()
            # ------------------------------------------
            # Control changes with previous generation
            if player in self.previous_generation and self.previous_generation[player] > 0:
                self.previous_generation[player] -= 1
            else:
                generation_changes += 1
            # Save current generation
            if player not in current_generation:
                current_generation[player] = 0
            current_generation[player] += 1
        
        # Update fitness values
        self.best_fit = best_fit
        self.worst_fit = worst_fit
        self.avg_fitness = sum_fitness / self.N

        # Update changes
        self.generation_changes = generation_changes
        self.previous_generation = current_generation

        # Update diversity
        self.diversity = len(current_generation) / self.N

    def is_algorithm_over(self):
        return any(stopper.is_algorithm_over(self) for stopper in self.function_config.stop_instance_list)

    def iterate(self):
        # Select K parents from player_collection
        parent_collection = self.function_config.parent_selectors.get_count(
            self.K, self.player_collection, self.generation_count)

        # Cross parents, generating K childs
        child_collection = []
        for i in range(0, self.K - 1, 2):
            child_collection.extend(self.function_config.crossover_function(
                parent_collection[i], parent_collection[i + 1]))
        # If last parent remained unmatched, add it to child collection
        if len(child_collection) != self.K:
            child_collection.append(parent_collection[self.K - 1])

        # Mutate each child
        mutated_child_collection = []
        for child in child_collection:
            mutated_child_collection.append(self.function_config.mutation_instance.mutate(child))

        # Choose N from N (actual) + K (childs) to save new generation
        if self.fill_all:
            self.player_collection = self.do_fill_all(mutated_child_collection)
        else:
            self.player_collection = self.do_fill_parent(mutated_child_collection)

        # Update general values
        self.generation_count += 1
        self.update_algo_stats()

        return self.player_collection

    def do_fill_all(self, child_collection):
        # Select N from N (actual) + K (childs)
        child_collection.extend(self.player_collection)
        return self.function_config.replace_selectors.get_count(
            self.N, child_collection, self.generation_count
        )
    
    def do_fill_parent(self, child_collection):
        if self.K > self.N:
            # Select N from K (childs)
            return self.function_config.replace_selectors.get_count(
                self.N, child_collection, self.generation_count
            )
        # K <= N
        # K childs + Select N-K from N (actual)
        child_collection.extend(self.function_config.replace_selectors.get_count(
            self.N - self.K, self.player_collection, self.generation_count
        ))
        return child_collection
