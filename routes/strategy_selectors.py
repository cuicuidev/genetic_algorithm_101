import streamlit as st
from abc import ABC

def crossoverStrategySelector(crossover_strategies):
    with st.expander(label = 'Crossover'):
        crossover_option = st.selectbox(label = 'Select strategy', options = list(crossover_strategies.keys()))
        crossover_strategy = crossover_strategies[crossover_option]

        if crossover_option == 'Uniform':
            binary = st.radio(label = 'Binary', options = [True, False])
            crossover_params = {'binary' : binary}
        
        if crossover_option == 'One Point':
            crossover_params = {}

        if crossover_option == 'Two Points':
            crossover_params = {}

        crossover_strategy = crossover_strategy(**crossover_params)

    return crossover_strategy

def mutationStrategySelector(mutation_strategies, chromosome_min_length, chromosome_max_length, gene_pool):
    with st.expander(label = 'Mutation'):
        mutation_option = st.selectbox(label = 'Select strategy', options = list(mutation_strategies.keys()))
        mutation_strategy = mutation_strategies[mutation_option]

        mutation_rate = st.slider(label = 'Mutation rate', min_value = 0.0, max_value = 1.0, step = 0.001, value = 0.05)
        severeness = st.slider(label = 'Severeness', min_value = 0.0, max_value = 1.0, step = 0.001, value = 0.5)

        if mutation_option == 'Delete':
            mutation_params = {'chromosome_min_length' : chromosome_min_length}

        if mutation_option == 'Flip':
            mutation_params = {'gene_pool' : gene_pool}

        if mutation_option == 'Swap':
            mutation_params = {}

        if mutation_option == 'Inverse':
            mutation_params = {}
        
        mutation_params['mutation_rate'] = mutation_rate
        mutation_params['severeness'] = severeness

        mutation_strategy = mutation_strategy(**mutation_params)
        
        

    return mutation_strategy

def replacementStrategySelector(replacement_strategies):
    with st.expander(label = 'Replacement'):
        replacement_option = st.selectbox(label = 'Select strategy', options = list(replacement_strategies.keys()))
        replacement_strategy = replacement_strategies[replacement_option]

        replacement_params = {}
        replacement_strategy = replacement_strategy(**replacement_params)

    return replacement_strategy


class StrategySelector(ABC):
    
    def __init__(self, strategies, descriptions, expander, expanded, label):
        self.strategies = strategies
        self.descriptions = descriptions
        self.expander = expander
        self.expanded = expanded
        self.label = label

    def render(self):
        return self._expander()

    def _expander(self):
        if self.expander:
            with st.expander(label = self.label, expanded = self.expanded):
                return self._selector()
        else:
            return self._selector()

    def _selector(self):
        pass

class InitializationSelector(StrategySelector):
    
    def __init__(self, gene_pool, strategies, descriptions = True, expander = True, expanded = False, label = 'Initialization'):
        super().__init__(strategies, descriptions, expander, expanded, label)
        self.gene_pool = gene_pool

    def _selector(self):

        if self.descriptions:
            st.markdown("Population initialization is the first step in any genetic algorithm. Given the gene pool, we can create individuals composed only by the genes specified. Some problems may requiere solutions variable in length. That's what the next two sliders are for, selecting the length constraints for individuals in the population.")
        
        min_chromosome_len = st.slider(label = 'Minimum length', min_value = 1, max_value = 100, value = 1)
        max_chromosome_len = st.slider(label = 'Maximum length', min_value = 1, max_value = 100, value = 100)

        
        if self.descriptions:
            st.markdown("Also, the population size itself may be variable, so we can define boundaries for that too. Some combination of strategies may drive a population to extinction; others, to exponential growth. In either case, if no boundaries are set, the algorithm will most likely fail.")
        
        min_population_size = st.slider(label = 'Minimum size', min_value = 50, max_value = 500, value = 50)
        max_population_size = st.slider(label = 'Maximum size', min_value = 50, max_value = 500, value = min_population_size)

        
        if self.descriptions:
            st.markdown("Finally, we must select the initialization strategy. By default, it's set to random for this demonstration, but feel free to select another strategy.")

        option = st.selectbox(label = 'Select strategy', options = list(self.strategies.keys()))
        strategy = self.strategies[option]

        params = {'gene_pool' : self.gene_pool,
                  'min_population_size' : min_population_size,
                  'max_population_size' : max_population_size,
                  'min_chromosome_length' : min_chromosome_len,
                  'max_chromosome_length' : max_chromosome_len,
                  }

        if option == 'Random':
            if self.descriptions:
                st.markdown("Random initialization is exactly what you think it is, we select a random population size and we fill it with individuals with random genes and lengths, all withing the constraints established earlier.")

        strategy = strategy(**params)
        return strategy


class SelectionSelector(StrategySelector):
    
    def __init__(self, fitness, fitness_params, min_population_size, strategies, descriptions = True, expander = True, expanded = False, label = 'Selection'):
        super().__init__(strategies, descriptions, expander, expanded, label)
        self.fitness = fitness
        self.fitness_params = fitness_params
        self.min_population_size = min_population_size
    
    def _selector(self):
        option = st.selectbox(label = 'Select strategy', options = list(self.strategies.keys()))
        strategy = self.strategies[option]

        total_pairs = st.slider(label = 'Parent pairings', min_value = 1, max_value = self.min_population_size*4, value = self.min_population_size)
        params = {'fitness' : self.fitness, 'fitness_params' : self.fitness_params, 'total_pairs' : total_pairs}
        
        if option == 'Tournament':
            k = st.slider(label = 'k', min_value = 1, max_value = self.min_population_size//4, value = self.min_population_size//40 + 1)
            params['k'] = k
        
        strategy = strategy(**params)
        return strategy

class CrossoverSelector(StrategySelector):
    pass

class MutationSelector(StrategySelector):
    pass

class ReplacementSelector(StrategySelector):
    pass

