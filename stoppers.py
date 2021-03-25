import time

# n will be used as first param for all methods
class Stopper(object):

    def __init__(self, n):
        self.n = n
    
    def is_algorithm_over(self, algo):
        pass

class TimeStopper(Stopper):
    def __init__(self, max_seconds):
        super().__init__(max_seconds)
    
    def is_algorithm_over(self, algo):
        return (time.time() - algo.start_time) > self.n

class GenerationCountStopper(Stopper):
    def __init__(self, max_count):
        super().__init__(max_count)
    
    def is_algorithm_over(self, algo):
        return algo.generation_count > self.n

# TODO: Implement is_algorithm_over
class AcceptableSolutionStopper(Stopper):
    def __init__(self, min_fitness):
        super().__init__(min_fitness)
    
    def is_algorithm_over(self, algo):
        pass

# TODO: Implement full
class StructuralStopper(Stopper):
    def __init__(self, generation_count, r):
        super().__init__(generation_count)
        self.r = r  # Relevant proportion of generation
        self.accum = 0
    
    def is_algorithm_over(self, algo):
        aux = 0
        for player in algo.player_collection:
            if not player.mutated: aux += 1     # ASUMIENDO QUE IMPLEMENTO ESE BOOLEAN
        if (aux/self.n) >= self.r:
            self.accum += 1
        return self.accum >= self.n

# TODO: Implement full
class ContentStopper(Stopper):
    def __init__(self, generation_count, max_count, algo):
        super().__init__(generation_count)
        self.max = max_count
        self.last_best = self.best_fitness(algo)
        self.accum = 0
    
    def is_algorithm_over(self, algo):
        best_player = self.best_fitness(algo)
        if(not best_player.mutated):            # y es el mismo que last_best
            self.accum += 1
        else:
            self.accum = 0
        return self.accum >= self.max


    def best_fitness(self, algo):
        best_player = algo.player_collection.first
        for player in algo.player_collection:
            if best_player.fitness < player.fitness:
                best_player = player
        return best_player