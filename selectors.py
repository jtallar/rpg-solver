import math
import random
import bisect

# Select K members from collection
class Selector(object):
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

        # Generate count times: rj = rj_function, take collection[i] : q[i-1] < r <= q[i]
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
        # Only one random, others depend on index and count
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
        # Save new fitness_prime value
        for index, el in enumerate(sorted_collection):
            el.fitness_prime = (len(sorted_collection) - index) / len(sorted_collection)

        # Roulette by fitness_prime
        return cls.base_roulette_selector(
            count, 
            collection, 
            lambda j, k, : random.random(),
            lambda el : el.fitness_prime
        )

    # Take count elements from collection using Boltzmann selector
    # Recieves additional param: temperature (Algorithm should go about modifying it)
    @classmethod
    def boltzmann_selector(cls, count, collection, temperature):
        # Calculate sum of exp_partial
        sum_exp_partial = 0
        for el in collection:
            el.exp_val = math.exp(el.fitness() / temperature)
            sum_exp_partial += el.exp_val
        
        # Calculate average exp_partial
        avg_exp_partial = sum_exp_partial / len(collection)

        # Save new exp_val value
        for el in collection:
            el.exp_val = el.exp_val / avg_exp_partial

        # Roulette by exp_val
        return cls.base_roulette_selector(
            count, 
            collection, 
            lambda j, k, : random.random(),
            lambda el : el.exp_val
        )
    
    # Take count elements from collection using Deterministic Tournament selector
    # Recieves additional param: M (M = 2 or M = 3 or similar)
    @classmethod
    def deterministic_tournament_selector(cls, count, collection, m):
        selected = []
        for index in range(count):
            # Select m random from collection (no repetition)
            m_elements = random.sample(collection, m)
            # Take the highest (fitness)
            selected.append(max(m_elements))

        return selected

    # Take count elements from collection using Probabilistic Tournament selector
    # Recieves additional param: threshold (threshold e [0.5, 1])
    @classmethod
    def probabilistic_tournament_selector(cls, count, collection, threshold):
        selected = []
        for index in range(count):
            # Select 2 random from collection (no repetition)
            m_elements = random.sample(collection, 2)
            # If r < Th, take fittest. Else, take worst. r e [0, 1)
            if random.random() < threshold:
                selected.append(max(m_elements))
            else:
                selected.append(min(m_elements))

        return selected


