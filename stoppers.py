import math
import time
import player as ply

# n will be used as first param for all methods
class Stopper(object):

    def __init__(self, n):
        self.n = n
    
    def is_algorithm_over(self, algo):
        pass

    @classmethod
    def is_param_list_valid(cls, param_list):
        return len(param_list) == 1 and param_list[0] > 0
    
    @classmethod
    def new_from_param_list(cls, param_list):
        return cls(param_list[0])

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return type(self).__name__

class TimeStopper(Stopper):
    def __init__(self, max_seconds):
        super().__init__(max_seconds)
    
    def is_algorithm_over(self, algo):
        algo.current_stopper = type(self).__name__
        return (time.time() - algo.start_time) >= self.n

    @classmethod
    def is_param_list_valid(cls, param_list):
        return super().is_param_list_valid(param_list)
    
    @classmethod
    def new_from_param_list(cls, param_list):
        return cls(param_list[0])
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return super().__repr__() + "(Target Seconds = %s)" % (self.n)

class GenerationCountStopper(Stopper):
    def __init__(self, max_count):
        super().__init__(int(max_count))
    
    def is_algorithm_over(self, algo):
        algo.current_stopper = type(self).__name__
        return algo.generation_count >= self.n

    @classmethod
    def is_param_list_valid(cls, param_list):
        return super().is_param_list_valid(param_list)
    
    @classmethod
    def new_from_param_list(cls, param_list):
        return cls(param_list[0])

    def __repr__(self):
        return super().__repr__() + "(Target Generations = %s)" % (self.n)

class DiversityStopper(Stopper):
    def __init__(self, min_diversity):
        super().__init__(min_diversity)
    
    def is_algorithm_over(self, algo):
        algo.current_stopper = type(self).__name__
        return algo.diversity <= self.n

    @classmethod
    def is_param_list_valid(cls, param_list):
        return super().is_param_list_valid(param_list) and param_list[0] <= 1
    
    @classmethod
    def new_from_param_list(cls, param_list):
        return cls(param_list[0])

    def __repr__(self):
        return super().__repr__() + "(Target Diversity = %s)" % (self.n)

class AcceptableSolutionStopper(Stopper):
    def __init__(self, min_fitness):
        super().__init__(min_fitness)
    
    def is_algorithm_over(self, algo):
        algo.current_stopper = type(self).__name__
        return algo.best_fit.fitness() >= self.n

    @classmethod
    def is_param_list_valid(cls, param_list):
        return super().is_param_list_valid(param_list)
    
    @classmethod
    def new_from_param_list(cls, param_list):
        return cls(param_list[0])

    def __repr__(self):
        return super().__repr__() + "(Target Fitness = %s)" % (self.n)

# Taking number of changes between Gn and Gn-1 (change defined by fitness)
class StructuralStopper(Stopper):
    def __init__(self, generation_count, r):
        super().__init__(int(generation_count))
        self.r = r  # Relevant proportion of generation
        self.repeated_part_count = 0
    
    def is_algorithm_over(self, algo):
        algo.current_stopper = type(self).__name__
        # Proportion of equal players from this gen to previous gen
        cur_maintain = (algo.N - algo.generation_changes) / algo.N
        if cur_maintain >= self.r:
            self.repeated_part_count += 1
        else:
            self.repeated_part_count = 0
        
        return self.repeated_part_count >= self.n

    @classmethod
    def is_param_list_valid(cls, param_list):
        # param[0] => n, param[1] => r
        return len(param_list) == 2 and param_list[0] >= 0 and param_list[1] > 0 and param_list[1] <= 1
    
    @classmethod
    def new_from_param_list(cls, param_list):
        return cls(param_list[0], param_list[1])
    
    def __repr__(self):
        return super().__repr__() + "(%s%% unchanged for %s generation/s)" % (self.r * 100, self.n)

# Taking fitness by value, can be different players
class ContentStopper(Stopper):
    def __init__(self, generation_count):
        super().__init__(int(generation_count))
        self.prev_best_fitness = float("Inf")
        self.repeated_best_count = 0
    
    def is_algorithm_over(self, algo):
        algo.current_stopper = type(self).__name__
        cur_best_fitness = algo.best_fit.fitness()
        if math.isclose(self.prev_best_fitness, cur_best_fitness, abs_tol=ply.Player.FIT_ABS_TOL):
            self.repeated_best_count += 1
        else:
            self.repeated_best_count = 0

        self.prev_best_fitness = cur_best_fitness
        return self.repeated_best_count >= self.n

    @classmethod
    def is_param_list_valid(cls, param_list):
        return super().is_param_list_valid(param_list)
    
    @classmethod
    def new_from_param_list(cls, param_list):
        return cls(param_list[0])

    def __repr__(self):
        return super().__repr__() + "(Target genertions = %s)" % (self.n)