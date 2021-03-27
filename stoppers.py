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
        return algo.best_fit >= self.n

# TODO: Implement full
class StructuralStopper(Stopper):
    def __init__(self, generation_count, r):
        super().__init__(generation_count)
        self.r = r  # Relevant proportion of generation
    
    def is_algorithm_over(self, algo):
        pass

# TODO: Implement full
class ContentStopper(Stopper):
    def __init__(self, generation_count):
        super().__init__(generation_count)
    
    def is_algorithm_over(self, algo):
        pass