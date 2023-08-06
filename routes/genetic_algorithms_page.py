import streamlit as st

def geneticAlgorithmsPage():
    st.title('Welcome!')

    st.write("If you are curious about machine learning and genetic algorithms, this is the rigth place for you. \
             Here you will learn everything you need to know to get started with genetic algorithms, so you can confidently design your own. \
             Not only you will walk out with good understanding of genetic algorithms, but also you will get a chance to play and interact \
             with an algorithm I've build for this site.")
    
    st.write("#### What are genetic algorithms?")
    st.write("In machine learning, a genetic algorithm is a heuristic algorithm inspired in the theory of evolution by natural selection. \
             Genetic algorithms are used to solve optimization problems and they are a great choice when the problem in question is of NP complexity, \
             but can be used for P complexity problems too.")
    st.write("Exactly as evolution occurs in nature, a genetic algorithm is aimed to simulate the process. When creating such an algorithm, we must have a population \
             (which often is initialized at random) and an environment (known as fitness function) that shapes the population over many generations. The population \
             is composed of individuals (potential solutions to the problem) that can reproduce to generate offspring. The offspring then may or may not \
             mutate, depending on a mutation chance specified beforehand. At last, a new generation is created with the offspring, and the whole process is repeated \
             again as many times as specified. Over time, the population converges to gradually better and better solutions to the problem.")
    st.write("An individual is defined by its chromosome. A chromosome is an array of elements (genes) that describe a unique solution to the problem. Let's define a problem, \
             for instance: We want to find the best way to pack a travel bag with items of different values, such that the items contained in the bag are of the \
             highest value possible. The bag can only hold a limited number of items, so we must choose which ones we want to keep and which ones will be discarted. \
             A chromosome would be an array of items and each item would be a gene.")