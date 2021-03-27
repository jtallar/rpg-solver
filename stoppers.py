import math
import time
import player as ply

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
        return (time.time() - algo.start_time) >= self.n

class GenerationCountStopper(Stopper):
    def __init__(self, max_count):
        super().__init__(max_count)
    
    def is_algorithm_over(self, algo):
        return algo.generation_count >= self.n

class AcceptableSolutionStopper(Stopper):
    def __init__(self, min_fitness):
        super().__init__(min_fitness)
    
    def is_algorithm_over(self, algo):
        return algo.best_fit.fitness() >= self.n

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

class ContentStopper(Stopper):
    def __init__(self, generation_count, max_count, algo):
        super().__init__(generation_count)
        self.prev_best_fitness = float("Inf")
        self.repeated_best_count = 0
    
    def is_algorithm_over(self, algo):
        cur_best_fitness = algo.best_fit.fitness()
        if math.isclose(self.prev_best_fitness, cur_best_fitness, abs_tol=ply.Player.FIT_ABS_TOL):
            self.repeated_best_count += 1
        else:
            self.repeated_best_count = 0

        self.prev_best_fitness = cur_best_fitness
        return self.repeated_best_count >= self.n