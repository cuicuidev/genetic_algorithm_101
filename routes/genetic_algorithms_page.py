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
    return int(string)

FITNESS_PARAMS = {}

GENES = '0123456789'

###################3

INITIALIZATIONS_STRATEGIES = {'Random' : RandomInitialization}
SELECTION_STRATEGIES = {'Tournament' : TournamentSelection, 'Roulette' : RouletteSelection}
CROSSOVER_STRATEGIES = {'Uniform' : UniformCrossover, 'One Point' : OnePointCrossover, 'Two Points' : TwoPointCrossover}
MUTATION_STRATEGIES = {'Pop' : PopMutation}
REPLACEMENT_STRATEGIES = {'Total' : TotalReplacement}
END_CONDITIONS = {'Generational' : None}

def geneticAlgorithmsPage():

    with open('routes/welcome_page.txt') as file:
        welcome = file.read()

    st.markdown(welcome)

    initialization_strategy = initializationStrategySelector(INITIALIZATIONS_STRATEGIES, GENES)

    min_population_size = initialization_strategy.min_population_size
    max_population_size = initialization_strategy.max_population_size
    min_chromosome_len = initialization_strategy.min_chromosome_length
    max_chromosome_len = initialization_strategy.max_chromosome_length

    st.markdown("##### Selection strategy")
    selection_strategy = selectionStrategySelector(SELECTION_STRATEGIES, fitness, FITNESS_PARAMS, min_population_size, max_population_size)

    st.markdown("##### Crossover strategy")
    crossover_strategy = crossoverStrategySelector(CROSSOVER_STRATEGIES)

    st.markdown("##### Mutation strategy")
    mutation_strategy = mutationStrategySelector(MUTATION_STRATEGIES, min_chromosome_len, max_chromosome_len)

    st.markdown("##### Replacement strategy")
    replacement_strategy = replacementStrategySelector(REPLACEMENT_STRATEGIES)

    model_params = {'initializationStrategy' : initialization_strategy,
            'selectionStrategy' : selection_strategy,
            'crossoverStrategy' : crossover_strategy,
            'mutationStrategy' : mutation_strategy,
            'replacementStrategy' : replacement_strategy,
            }
    
    st.markdown("##### End condition")
    with st.expander(label = 'Number of generations'):
        n_generations = st.slider(label = 'Generations', min_value = 1, max_value = 1000, value = 100)

    if st.button(label = 'Train'):
        gen = GeneticAlgorithm(fitness = fitness, fitness_params = FITNESS_PARAMS, genes = GENES)
        gen.setParams(**model_params)
        gen.initPopulation()
        gen.train(n_generations = n_generations)

        st.dataframe(data = [gen.bestIndividual, gen.bestScore])