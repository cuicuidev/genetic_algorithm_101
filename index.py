import streamlit as st
import plotly.express as px
import pandas as pd
from model import RegExPatternFinder
from testcases import TEST_CASES

def main():

    st.title('RegEx genetic algorithm!')

    with st.expander(label = 'Parameters'):
        population_size = st.slider(label = 'Population Size', min_value = 10, max_value = 10_000, value = 1_000)
        mutation_rate = st.slider(label = 'Mutation Rate', min_value = 0.0, max_value = 1.0, value = 0.05)
        hostility = st.slider(label = 'Environment Hostility', min_value = 0.0, max_value = 1.0, value = 0.5)
    
    if st.button(label = 'Train'):
        regex = RegExPatternFinder(mutation_rate = mutation_rate, hostility = hostility)
        regex.initPopulation(size = population_size)
        regex.setTestCases(test_cases = TEST_CASES)
        regex.train()

        st.dataframe(pd.DataFrame(regex.history))

if __name__ == '__main__':
    main()