import streamlit as st
import re
from model.model import GeneticAlgorithm
from model.strategies.crossover import *
from model.strategies.initialization import *
from model.strategies.mutation import *
from model.strategies.replacement import *
from model.strategies.selection import *
from routes.strategy_selectors import *

from test_cases import TEST_CASES

# def fitness(string, test_cases):
#     iters = len(test_cases)
    
#     score = 0
#     try:
#         for key, value in test_cases.items():
#             score += int(bool(re.match(string, key)) == value)
#     except:
#         return -1
#     return score / iters

# FITNESS_PARAMS = {'test_cases' : TEST_CASES}

# GENES = ''.join([chr(x) for x in range(32,126)])


###################3

def fitness(string):
    max_length = 100
    max_ = int('9'*max_length)
    return int(string) / max_

FITNESS_PARAMS = {}

GENES = '0123456789'

###################3

INITIALIZATIONS_STRATEGIES = {'Random' : RandomInitialization}
SELECTION_STRATEGIES = {'Tournament' : TournamentSelection, 'Roulette' : RouletteSelection}
CROSSOVER_STRATEGIES = {'Uniform' : UniformCrossover, 'One Point' : OnePointCrossover, 'Two Points' : TwoPointCrossover}
MUTATION_STRATEGIES = {'Delete' : DeleteMutation, 'Flip' : FlipMutation, 'Swap' : SwapMutation, 'Inverse' : InverseMutation}
REPLACEMENT_STRATEGIES = {'Total' : TotalReplacement}
END_CONDITIONS = {'Generational' : None}

def geneticAlgorithmsPage():

    with open('welcome_page.txt') as file:
        welcome = file.read()

    st.markdown(welcome)

    initialization_strategy = InitializationSelector(GENES, INITIALIZATIONS_STRATEGIES, expander = False).render()

    min_population_size = initialization_strategy.min_population_size
    max_population_size = initialization_strategy.max_population_size
    min_chromosome_len = initialization_strategy.min_chromosome_length
    max_chromosome_len = initialization_strategy.max_chromosome_length

    selection_strategy = SelectionSelector(fitness, FITNESS_PARAMS, min_population_size, SELECTION_STRATEGIES, expander = False).render()

    crossover_strategy = CrossoverSelector(CROSSOVER_STRATEGIES, expander = False).render()

    mutation_strategy = MutationSelector(GENES, min_chromosome_len, MUTATION_STRATEGIES, expander = False).render()

    replacement_strategy = ReplacementSelector(REPLACEMENT_STRATEGIES, expander = False).render()

    model_params = {'initializationStrategy' : initialization_strategy,
            'selectionStrategy' : selection_strategy,
            'crossoverStrategy' : crossover_strategy,
            'mutationStrategy' : mutation_strategy,
            'replacementStrategy' : replacement_strategy,
            }

    with st.expander(label = 'Number of generations'):
        n_generations = st.slider(label = 'Generations', min_value = 1, max_value = 1000, value = 100)

    if st.button(label = 'Train'):
        gen = GeneticAlgorithm(fitness = fitness, fitness_params = FITNESS_PARAMS, genes = GENES)
        gen.setParams(**model_params)
        gen.initPopulation()
        gen.train(n_generations = n_generations)

        st.dataframe(data = [gen.bestIndividual, gen.bestScore])
        st.dataframe(data = [gen.medianIndividual, gen.medianScore])