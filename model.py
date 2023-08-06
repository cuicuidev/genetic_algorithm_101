from typing import Callable
import random
import pandas as pd

class GeneticAlgorithm:

    def __init__(self, fitness: Callable[..., float], fitness_params: dict, genes: str):
        # constructor params
        self.fitness = fitness # fitness function takes in a string and returns a float between -1 and 1
        self.fitness_params = fitness_params # dictionary that resembles the parameters that might be passed down to the fitness function
        self.genes = genes # a string composed of the genes each individual might have
        
        # model params
        self.populationSize = None
        
        self.chromosomeMinLength = None
        self.chromosomeMaxLength = None
        
        self.selectionStrategy = None
        self.crossoverStrategy = None
        self.mutationStrategy = None
        self.replacementStrategy = None
        
        # object attributes
        self.generation = 0
        self.version = 1.0
        
        self.bestIndividual = ''
        self.medianIndividual =''
        
        self.currentPopulation = []
        self.currentFitnessScores = []
        
        self.history = {'generation' : [], 'version' : [], 'bestIndividual' : [], 'bestScore' : [], 'medianIndividual' : [], 'medianScore' : [], 'params' : []}
        
    def setParams(self, **kwargs):
        if self._initialized():
            self._updateVersion()
            
        self.populationSize = kwargs.get('populationSize', self.populationSize)
        self.chromosomeMinLength = kwargs.get('chromosomeMinLength', self.chromosomeMinLength)
        self.chromosomeMaxLength = kwargs.get('chromosomeMaxLength', self.chromosomeMaxLength)
        self.selectionStrategy = kwargs.get('selectionStrategy', self.selectionStrategy)
        self.crossoverStrategy = kwargs.get('crossoverStrategy', self.crossoverStrategy)
        self.mutationStrategy = kwargs.get('mutationStrategy', self.mutationStrategy)
        self.replacementStrategy = kwargs.get('replacementStrategy', self.replacementStrategy)
        
    def initPopulation(self):
        population = []
        for i in range(self.populationSize):
            chromosome_size = random.randint(self.chromosomeMinLength, self.chromosomeMaxLength)
            chromosome = ''.join([random.choice(self.genes) for x in range(chromosome_size)])
            population.append(chromosome)
        self.currentPopulation = population.copy()
        
    def _initialized(self):
        return self.populationSize is not None
        
    def _updateVersion(self):
        self.version += 0.1
        
    def _evaluatePopulation(self):
        scores = []
        for individual in self.currentPopulation:
            score = self.fitness(individual, **self.fitness_params)
            scores.append(score)
        self.currentFitnessScores = scores.copy()
    
    def _sortPopulation(self):
        self._evaluatePopulation()
        sorted_population, sorted_fitness_scores = zip(*sorted(zip(self.currentPopulation, self.currentFitnessScores), key=lambda x: x[1]))
        self.currentPopulation = list(sorted_population)
        self.currentScores = list(sorted_fitness_scores)
        
    ################################### SELECTION
        
    def _selection(self):
        return self.selectionStrategy.apply(self.currentPopulation)
    
    ################################### CROSSOVER
        
    def _crossover(self):
        return self.crossoverStrategy.apply(self._selection())
    
    ################################### MUTATION
    
    def _mutation(self, children):
        
        mutated_children = []
        
        for child in children:
            mutated_children.append(self._popMutation(child, **self.mutationStrategy['params']))
        
        return mutated_children
    
    def _popMutation(self, child, mutation_rate):
        max_index = len(child) - 1
        if random.random() < mutation_rate:
            index = random.randint(0, max_index)
            mutated_child = child[:index] + child[index + 1:]
            return mutated_child if len(mutated_child) > self.chromosomeMinLength else child
        return child
            

    ################################### REPLACEMENT
    
    def _replacement(self, children):
        self._totalReplacement(children)
        
    def _totalReplacement(self, children):
        self.currentPopulation = children
    
    ###################################
    
    def _logHistory(self):
        params = {'populationSize' : self.populationSize,
                  'chromosomeMinLength' : self.chromosomeMinLength,
                  'chromosomeMaxLength' : self.chromosomeMaxLength,
                  'selectionStrategy' : self.selectionStrategy,
                  'crossoverStrategy' : self.crossoverStrategy,
                  'mutationStrategy' : self.mutationStrategy,
                  'replacementStrategy' : self.replacementStrategy,
                 }
        
        self.history['generation'].append(self.generation)
        self.history['version'].append(self.version)
        self.history['bestIndividual'].append(self.bestIndividual)
        self.history['bestScore'].append(self.fitness(self.bestIndividual, **self.fitness_params))
        self.history['medianIndividual'].append(self.medianIndividual)
        self.history['medianScore'].append(self.fitness(self.medianIndividual, **self.fitness_params))
        self.history['params'].append(params)
    
    def train(self, n_generations):
        for n in range(n_generations):
            self._replacement(self._mutation(self._crossover()))
            
            self._sortPopulation()
            
            self.bestIndividual = self.currentPopulation[0]
            self.medianIndividual = self.currentPopulation[self.populationSize//2]
            self.generation += 1
            
            self._logHistory()
        
    def historyToPandas(self):
        return pd.DataFrame(self.history)