import streamlit as st
import plotly.express as px
import pandas as pd
from generalized import GeneticAlgorithm
from example import FITNESS, FITNESS_PARAMS, GENES

def main():

    st.title("Let's learn genetic algorithms")

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