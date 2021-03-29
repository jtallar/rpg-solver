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

# Taking number of changes between Gn and Gn-1 (change defined by fitness)
class StructuralStopper(Stopper):
    def __init__(self, generation_count, r):
        super().__init__(generation_count)
        self.r = r  # Relevant proportion of generation
        self.repeated_part_count = 0
    
    def is_algorithm_over(self, algo):
        # Proportion of equal players from this gen to previous gen
        cur_maintain = (algo.N - algo.generation_changes) / algo.N
        if cur_maintain >= self.r:
            self.repeated_part_count += 1
        else:
            self.repeated_part_count = 0
        
        return self.repeated_part_count >= self.n

# Taking fitness by value, can be different players
class ContentStopper(Stopper):
    def __init__(self, generation_count):
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