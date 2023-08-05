import streamlit as st
import plotly.express as px
import pandas as pd
from model import GeneticAlgorithm
from example import FITNESS, FITNESS_PARAMS, GENES

def main():

    st.title("Let's learn genetic algorithms")

    st.header("Frist, let'ss define a fitness function!")
    st.write("The function must have at least one parameter called 'string' and the output must be a float between -1 and 1.")
    st.write('This is a predefined example fitness function that takes as an input the previously mentioned string, and also a test_cases dictionary. \
             The function returns the ratio of test cases passed over all test cases. \
             The assertion is whether the string is a good regex pattern fit for a particular test case. \
             If the string cannot be used in regex, the function returns a fitness score of -1.')
    st.write('Basically, we are trying to see if the algorithm can arrive to a good regex pattern to fit the test cases specified.')
    st.write('This is the function we will be using...')

    with open('example_fitness.py') as file:
        example_fitness = file.read()

    st.code(body = example_fitness, language = 'python')

    st.write('... or you can write your own function instead!')

    fitness_function_boilerplate = 'def fitness(string: str):\n\
    # your code\n\n\
    return score'
    st.text_area(label = 'custom code', placeholder = fitness_function_boilerplate, label_visibility = 'collapsed', height = 120)

    with st.expander(label = 'Parameters'):
        populationSize = st.slider(label = 'Population Size', min_value = 10, max_value = 10_000, value = 1_000)
        chromosomeMinLength = st.slider(label = 'Min Chromosome Length', min_value = 1, max_value = 100, value = 1)
        chromosomeMaxLength = st.slider(label = 'Max Chromosome Length', min_value = 1, max_value = 100, value = 30)
        selectionStrategyStrategy = st.selectbox(label = 'Selection Strategy', options = ['tournament'])
        selectionStrategyParams = {'k' : 5}
        selectionStrategy = {'strategy' : selectionStrategyStrategy, 'params' : selectionStrategyParams}

        mutationStrategyStrategy = st.selectbox(label = 'Mutation Strategy', options = ['pop'])
        mutation_rate = st.slider(label = 'Mutation Rate', min_value = 0.0, max_value = 1.0, value = 0.05)
        mutationStrategyParams = {'mutation_rate' : mutation_rate}
        mutationStrategy = {'strategy' : mutationStrategyStrategy, 'params' : mutationStrategyParams}

        fitness = FITNESS
        fitness_params = FITNESS_PARAMS
        genes = GENES
        params = {'populationSize' : populationSize,
                  'chromosomeMinLength' : chromosomeMinLength,
                  'chromosomeMaxLength' : chromosomeMaxLength,
                  'selectionStrategy' : selectionStrategy,
                  'mutationStrategy' : mutationStrategy,
                  }
        
        n_generations = st.slider(label = 'Generations', min_value = 1, max_value = 1000, value = 100)
        
    
    if st.button(label = 'Train'):
        gen = GeneticAlgorithm(fitness = fitness, fitness_params = fitness_params, genes = genes)
        gen.setParams(**params)
        gen.initPopulation()
        gen.train(n_generations = n_generations)

        st.dataframe(gen.historyToPandas())

if __name__ == '__main__':
    main()