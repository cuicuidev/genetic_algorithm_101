import streamlit as st

def initializationStrategySelector(initialization_strategies, gene_pool):
    with st.expander(label = 'Intialization strategy'):
        initialization_option = st.selectbox(label = 'Initialization Strategy', options = list(initialization_strategies.keys()))
        initialization_strategy = initialization_strategies[initialization_option]

        if initialization_option == 'Random':
            min_chromosome_len = st.slider(label = 'Minimum length', min_value = 1, max_value = 100, value = 1)
            max_chromosome_len = st.slider(label = 'Maximum length', min_value = 1, max_value = 100, value = 100)
            min_population_size = st.slider(label = 'Minimum size', min_value = 50, max_value = 500, value = 50)
            max_population_size = st.slider(label = 'Maximum size', min_value = 50, max_value = 500, value = min_population_size)
            initialization_params = {'gene_pool' : gene_pool, 'min_population_size' : min_population_size, 'max_population_size' : max_population_size,
                                     'min_chromosome_length' : min_chromosome_len, 'max_chromosome_length' : max_chromosome_len,
                                     }
        initialization_strategy = initialization_strategy(**initialization_params)
    return initialization_strategy

def selectionStrategySelector(selection_strategies, fitness, fitness_params, min_population_size, max_population_size):
    with st.expander(label = 'Selection strategy'):
        selection_option = st.selectbox(label = 'Selection Strategy', options = list(selection_strategies.keys()))
        selection_strategy = selection_strategies[selection_option]
        
        if selection_option == 'Tournament':
            tournament_k_param = st.slider(label = 'k', min_value = 1, max_value = min_population_size//4, value = min_population_size//40 + 1)
            tournament_total_pairs = st.slider(label = 'total_pairs', min_value = 1, max_value = min_population_size*4, value = min_population_size)
            selection_params = {'k' : tournament_k_param, 'fitness' : fitness, 'fitness_params' : fitness_params, 'total_pairs' : tournament_total_pairs}

        if selection_option == 'Roulette':
            roulette_total_pairs = st.slider(label = 'total_pairs', min_value = 1, max_value = min_population_size*4, value = min_population_size)
            selection_params = {'fitness' : fitness, 'fitness_params' : fitness_params, 'total_pairs' : roulette_total_pairs}
        
        selection_strategy = selection_strategy(**selection_params)
    return selection_strategy

def crossoverStrategySelector(crossover_strategies):
    with st.expander(label = 'Crossover strategy'):
        crossover_option = st.selectbox(label = 'Crossover Strategy', options = list(crossover_strategies.keys()))
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

def mutationStrategySelector(mutation_strategies, chromosome_min_length, chromosome_max_length):
    with st.expander(label = 'Mutation strategy'):
        mutation_option = st.selectbox(label = 'Mutation Strategy', options = list(mutation_strategies.keys()))
        mutation_strategy = mutation_strategies[mutation_option]

        mutation_rate = st.slider(label = 'Mutation rate', min_value = 0.0, max_value = 1.0, step = 0.001, value = 0.05)

        if mutation_option == 'Pop':
            mutation_params = {'chromosome_min_length' : chromosome_min_length}
        
        mutation_params['mutation_rate'] = mutation_rate

        mutation_strategy = mutation_strategy(**mutation_params)

    return mutation_strategy

def replacementStrategySelector(replacement_strategies):
    with st.expander(label = 'Replacement strategy'):
        replacement_option = st.selectbox(label = 'Replacement Strategy', options = list(replacement_strategies.keys()))
        replacement_strategy = replacement_strategies[replacement_option]

        replacement_params = {}
        replacement_strategy = replacement_strategy(**replacement_params)

    return replacement_strategy