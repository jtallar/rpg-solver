import math
import random
import bisect

# Select K members from collection
class Selector(object):
    def __init__(self, K):
        self.K = K

    # Take count elements from collection using Elite selector
    @classmethod
    def elite_selector(cls, count, collection):
        # Sort by fitness (higher to lower)
        sorted_collection = sorted(collection, reverse=True)

        selected = []
        for index, element in enumerate(sorted_collection):
            # Take each element num times
            num = math.ceil((count - index) / len(collection))
            if num == 0: break
            selected.extend([element] * num)

        return selected
    
    # Generic Roulette method to use in various selectors
    @classmethod
    def base_roulette_selector(cls, count, collection, rj_function, fitness_function):
        # Calculate sum of fitness
        sum_fitness = 0
        for el in collection:
            sum_fitness += fitness_function(el)
        
        # Get relative fitness and save acum in q_list
        accum_rel_fitness = 0
        q_list = []
        for el in collection:
            accum_rel_fitness += fitness_function(el) / sum_fitness
            q_list.append(accum_rel_fitness)

        # Generate count times: rj = rand [0,1), take collection[i] : q[i-1] < r <= q[i]
        selected = []
        for j in range(count):
            rj = rj_function(j, count)
            # Perform binary search on q_list, q_list already sorted
            selected.append(collection[bisect.bisect_left(q_list, rj)])
        
        return selected

    # Take count elements from collection using Roulette selector
    @classmethod
    def roulette_selector(cls, count, collection):
        return cls.base_roulette_selector(
            count, 
            collection, 
            lambda j, k, : random.random(),
            lambda el : el.fitness()
        )
    
    # Take count elements from collection using Universal selector
    @classmethod
    def universal_selector(cls, count, collection):
        r = random.random()
        return cls.base_roulette_selector(
            count, 
            collection, 
            lambda j, k, r=r : (r + j) / k,
            lambda el : el.fitness()
        )

    # Take count elements from collection using Ranking selector
    @classmethod
    def ranking_selector(cls, count, collection):
        # Sort by fitness (higher to lower)
        sorted_collection = sorted(collection, reverse=True)
        for index, el in enumerate(sorted_collection):
            el.fitness_prime = (len(sorted_collection) - index) / len(sorted_collection)

        return cls.base_roulette_selector(
            count, 
            collection, 
            lambda j, k, : random.random(),
            lambda el : el.fitness_prime
        )



