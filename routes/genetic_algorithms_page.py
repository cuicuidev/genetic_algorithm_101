import streamlit as st
import re
from model.model import GeneticAlgorithm
from routes.strategy_selectors import *
from model.strategies.strategies import *

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

SELECTION_STRATEGIES = {'Tournament' : TournamentSelection, 'Roulette' : RouletteSelection}
CROSSOVER_STRATEGIES = {'Uniform' : UniformCrossover, 'One Point' : OnePointCrossover, 'Two Points' : TwoPointCrossover}
MUTATION_STRATEGIES = {'Pop' : PopMutation}
REPLACEMENT_STRATEGIES = {'Total' : TotalReplacement}

def geneticAlgorithmsPage():

    with open('routes/welcome_page.txt') as file:
        welcome = file.read()

    st.markdown(welcome)
    min_chromosome_len = st.slider(label = 'Minimum length', min_value = 1, max_value = 100, value = 1)
    max_chromosome_len = st.slider(label = 'Maximum length', min_value = 1, max_value = 100, value = 100)

    st.markdown("Now that we've stated the problem, it's time to choose strategies for selection, crossover, mutation and replacement. But first, let's define the minimum and maximum population size")

    min_population_size = st.slider(label = 'Minimum size', min_value = 50, max_value = 500, value = 50)
    max_population_size = st.slider(label = 'Maximum size', min_value = 50, max_value = 500, value = min_population_size)

    st.markdown("##### Selection strategy")
    selection_strategy = selectionStrategySelector(SELECTION_STRATEGIES, fitness, FITNESS_PARAMS, min_population_size, max_population_size)

    st.markdown("##### Crossover strategy")
    crossover_strategy = crossoverStrategySelector(CROSSOVER_STRATEGIES)

    st.markdown("##### Mutation strategy")
    mutation_strategy = mutationStrategySelector(MUTATION_STRATEGIES, min_chromosome_len, max_chromosome_len)

    st.markdown("##### Replacement strategy")
    replacement_strategy = replacementStrategySelector(REPLACEMENT_STRATEGIES)

    model_params = {'populationSize' : min_population_size,
            'chromosomeMinLength' : min_chromosome_len,
            'chromosomeMaxLength' : max_chromosome_len,
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

        st.dataframe(data = gen.historyToPandas())