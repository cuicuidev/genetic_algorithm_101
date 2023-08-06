import streamlit as st
from benchmarking import measureExecTime
from example_fitness import *
from test_cases import TEST_CASES
from RestrictedPython import safe_builtins, limited_builtins, utility_builtins, compile_restricted
from RestrictedPython.Eval import default_guarded_getiter
from RestrictedPython.Guards import guarded_iter_unpack_sequence, full_write_guard

FITNESS_PARAMS = {'test_cases' : TEST_CASES}

GENES = ''.join([chr(x) for x in range(32,126)])

def getFitness():
    st.write("##### Frist, let's define a fitness function!")
    st.write('This is a predefined example fitness function that takes as an input the previously mentioned string, and also a test_cases dictionary. \
             The function returns the ratio of test cases passed over all test cases. \
             The assertion is whether the string is a good regex pattern fit for a particular test case. \
             If the string cannot be used in regex, the function returns a fitness score of -1.')
    st.write('Basically, we are trying to see if the algorithm can arrive to a good regex pattern to fit the test cases specified.')

    with open('example_fitness.py') as file:
        example_fitness = file.read()

    st.code(body = example_fitness, language = 'python')

    # st.write('... or you can write your own function instead!')

    # fitness_function_boilerplate = 'def fitness(string: str):\n\
    #     # your code\n\n\
    #     return score'

    # with st.expander(label = 'Open text field'):
    #     st.selectbox(label = 'language', options = ['python'])
    #     custom_fitness = st.text_area(label = 'custom code', placeholder = fitness_function_boilerplate, label_visibility = 'collapsed', height = 300)

    #     code = compile_restricted(
    #         custom_fitness,
    #         filename='<string>',
    #         mode='exec'
    #     )
    #     restricted_locals = {}
    #     restricted_globals = {
    #         '__builtins__': {**safe_builtins, 'range' : range},
    #         '___getiter___': default_guarded_getiter,
    #         'iter_unpack_sequence': guarded_iter_unpack_sequence,
    #         '_write_': full_write_guard,
    #     }

    #     exec(code, restricted_globals, restricted_locals)
    #     custom_func = restricted_locals.get('fitness')
    #     custom_params = restricted_locals.get('params')
    #     custom_genes = restricted_locals.get('genes')
    
    # if custom_func:
    #     fitness_ = custom_func
    #     benchmark_params = custom_params
    #     benchmark_params['string'] = custom_genes

    fitness_ = fitness
    benchmark_params = FITNESS_PARAMS
    benchmark_params['string'] = GENES
    
    fitness_exec_time = measureExecTime(fitness_, iters = 1000, **benchmark_params)*1000
    st.write(f'Expected execution time: {fitness_exec_time:.4f} ms')

    return fitness_, GENES, FITNESS_PARAMS