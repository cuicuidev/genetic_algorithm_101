import streamlit as st
import pandas as pd
from model import GeneticAlgorithm
from benchmarking import *
from fitness import getFitness

def aSimpleExamplePage():

    st.title('Experiment with a genetic algorithm!')

    fitness, genes, fitness_params = getFitness()

    ####################################### PARAMS
    st.write("Now, let's define some basic algorithm parameters!")

    with st.expander(label = 'Population Size'):
        st.write('This parameter defines how large the population must be. As the population increases, \
                                   so does the model performance, but the training time also grows large.')
        populationSize = st.slider(label = 'size',
                                   min_value = 10,
                                   max_value = 10_000,
                                   value = 1_000)
        
    with st.expander(label = 'Chromosome length'):
        st.write('Min and max chromosome length')
        chromosomeMinLength = st.slider(label = 'Min Chromosome Length', min_value = 1, max_value = 100, value = 1)
        chromosomeMaxLength = st.slider(label = 'Max Chromosome Length', min_value = 1, max_value = 100, value = 30)
        possible_fenotypes = calculatePhenotypes(genes, chromosomeMinLength, chromosomeMaxLength)
        st.write(f'Possible unique individuals: {possible_fenotypes}')
    
    with st.expander(label = 'Selection Strategy'):
        selectionStrategyStrategy = st.selectbox(label = 'Selection Strategy', options = ['tournament'])
        selectionStrategyParams = {'k' : 5}
        selectionStrategy = {'strategy' : selectionStrategyStrategy, 'params' : selectionStrategyParams}

    with st.expander(label = 'Mutation Strategy'):
        mutationStrategyStrategy = st.selectbox(label = 'Mutation Strategy', options = ['pop'])
        mutation_rate = st.slider(label = 'Mutation Rate', min_value = 0.0, max_value = 1.0, value = 0.05)
        mutationStrategyParams = {'mutation_rate' : mutation_rate}
        mutationStrategy = {'strategy' : mutationStrategyStrategy, 'params' : mutationStrategyParams}

        params = {'populationSize' : populationSize,
                  'chromosomeMinLength' : chromosomeMinLength,
                  'chromosomeMaxLength' : chromosomeMaxLength,
                  'selectionStrategy' : selectionStrategy,
                  'mutationStrategy' : mutationStrategy,
                  }
    with st.expander(label = 'Number of generations'):
        n_generations = st.slider(label = 'Generations', min_value = 1, max_value = 1000, value = 100)
        
    
    if st.button(label = 'Train'):
        gen = GeneticAlgorithm(fitness = fitness, fitness_params = fitness_params, genes = genes)
        gen.setParams(**params)
        gen.initPopulation()
        gen.train(n_generations = n_generations)

        st.dataframe(data = gen.historyToPandas())