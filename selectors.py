import math
import random
import bisect

# Select K members from collection
class Selector(object):
    def select(self, count, collection):
        pass

# Take count elements from collection using Elite selector
class EliteSelector(Selector):
    def select(self, count, collection):
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
class BaseRouletteSelector(Selector):
    def select(self, count, collection, rj_function, fitness_function):
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
class RouletteSelector(BaseRouletteSelector):
    def select(self, count, collection):
        return super().select(
            count, 
            collection, 
            lambda j, k, : random.random(),
            lambda el : el.fitness()
        )

# Take count elements from collection using Universal selector
class UniversalSelector(BaseRouletteSelector):
    def select(self, count, collection):
        # Only one random, others depend on index and count
        r = random.random()
        return super().select(
            count, 
            collection, 
            lambda j, k, r=r : (r + j) / k,
            lambda el : el.fitness()
        )

# Take count elements from collection using Ranking selector
class RankingSelector(BaseRouletteSelector):
    def select(self, count, collection):
        # Sort by fitness (higher to lower)
        sorted_collection = sorted(collection, reverse=True)
        # Save new fitness_prime value
        for index, el in enumerate(sorted_collection):
            el.fitness_prime = (len(sorted_collection) - index) / len(sorted_collection)

        # Roulette by fitness_prime
        return super().select(
            count, 
            collection, 
            lambda j, k, : random.random(),
            lambda el : el.fitness_prime
        )

# Take count elements from collection using Boltzmann selector
# Recieves additional constructor params: init_temperature and end_temperature
# Recieves additional param: time (Algorithm should go about modifying it)
class BoltzmannSelector(BaseRouletteSelector):
    k_factor = 0.2

    def __init__(self, init_temperature, end_temperature):
        self.init_temperature = init_temperature
        self.end_temperature = end_temperature

    def temperature(self, time):
        return self.end_temperature + (self.init_temperature - self.end_temperature) * math.exp(-self.k_factor * time)

    # TODO: Ver si time es numero de generacion o tiempo en segundos
    def select(self, count, collection, time):
        # Calculate temperature
        temperature = self.temperature(time)
        # Calculate sum of exp_partial
        sum_exp_partial = 0
        for el in collection:
            el.exp_val_partial = math.exp(el.fitness() / temperature)
            sum_exp_partial += el.exp_val_partial
        
        # Calculate average exp_partial
        avg_exp_partial = sum_exp_partial / len(collection)

        # Save new exp_val value
        for el in collection:
            el.exp_val = el.exp_val_partial / avg_exp_partial

        # Roulette by exp_val
        return super().select(
            count, 
            collection, 
            lambda j, k, : random.random(),
            lambda el : el.exp_val
        )

# Take count elements from collection using Deterministic Tournament selector
# Recieves constructor param: M (M = 2 or M = 3 or similar)
class DeterministicTournamentSelector(Selector):
    def __init__(self, M):
        self.M = M
    
    def select(self, count, collection):
        selected = []
        for index in range(count):
            # Select M random from collection (no repetition)
            m_elements = random.sample(collection, self.M)
            # Take the highest (fitness)
            selected.append(max(m_elements))

        return selected

# Take count elements from collection using Probabilistic Tournament selector
# Recieves additional constructor param: threshold (threshold e [0.5, 1])
class ProbabilisticTournamentSelector(Selector):
    def __init__(self, threshold):
        self.threshold = threshold
    
    def select(self, count, collection):
        selected = []
        for index in range(count):
            # Select 2 random from collection (no repetition)
            m_elements = random.sample(collection, 2)
            # If r < Th, take fittest. Else, take worst. r e [0, 1)
            if random.random() < self.threshold:
                selected.append(max(m_elements))
            else:
                selected.append(min(m_elements))

        return selected

# Select K members from collection
class SelectorFunctions(object):
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

class CombinedSelector(object):
    def __init__(self, method_1_instance, method_2_instance, percentage_m1):
        """Returns a Combined Selector object with given methods
        
        Parameters
        ----------
        method1 : Selector
            Instance from Selector son class
        method2 : Selector
            Instance from Selector son class
        percentage_m1 : float e [0;1]
            Percentage of selections to take from method 1.
        """
        self.method_1_instance = method_1_instance
        self.method_2_instance = method_2_instance
        self.percentage_m1 = percentage_m1
    
    def get_count(self, count, collection, time=0):
        # Take percentage_m1 * count from method 1 and (1 - percentage_m1) from methodd 2
        # param_m1 or param_m2 might be 0, check with is not None
        first_sel = second_sel = []
        count_m1 = round(count * self.percentage_m1)
        count_m2 = count - count_m1

        # Skip a method if its count is 0
        if count_m1:
            first_sel = self.apply_method(self.method_1_instance, count_m1, collection, time)
        if count_m2:
            second_sel = self.apply_method(self.method_2_instance, count_m2, collection, time)

        first_sel.extend(second_sel)
        return first_sel

    def apply_method(self, method_instance, count, collection, time):
        if type(method_instance) == BoltzmannSelector:
            return method_instance.select(count, collection, time)
        return method_instance.select(count, collection)

