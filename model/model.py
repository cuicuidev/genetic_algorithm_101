from logging import Logger
from typing import Callable

class GeneticAlgorithm:

    def __init__(self, fitness: Callable[..., float], fitness_params: dict, genes: str):
        # constructor params
        self.fitness = fitness # fitness function takes in a string and returns a float between -1 and 1
        self.fitness_params = fitness_params # dictionary that resembles the parameters that might be passed down to the fitness function
        self.genes = genes # a string composed of the genes each individual might have
        
        # model params
        self.initializationStrategy = None
        self.selectionStrategy = None
        self.crossoverStrategy = None
        self.mutationStrategy = None
        self.replacementStrategy = None
        self.endCondition = None
        
        # object attributes
        self.generation = 0
        self.version = 1.0
        
        self.bestIndividual = ''
        self.bestScore = 0
        self.medianIndividual = ''
        self.medianScore = 0
        
        self.currentPopulation = []
        self.currentFitnessScores = []

        self.logger = Logger(self)
        
    def setParams(self, **kwargs):
        if self._initialized():
            self._updateVersion()
            
        self.initializationStrategy = kwargs.get('initializationStrategy', self.initializationStrategy)
        self.selectionStrategy = kwargs.get('selectionStrategy', self.selectionStrategy)
        self.crossoverStrategy = kwargs.get('crossoverStrategy', self.crossoverStrategy)
        self.mutationStrategy = kwargs.get('mutationStrategy', self.mutationStrategy)
        self.replacementStrategy = kwargs.get('replacementStrategy', self.replacementStrategy)
        self.endCondition = kwargs.get('endCondition', self.endCondition)
        
    def initPopulation(self):
        self.currentPopulation = self.initializationStrategy.apply()
        
    def _initialized(self):
        return self.initializationStrategy is not None
        
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
        self.currentPopulation = list(sorted_population)[::-1]
        self.currentScores = list(sorted_fitness_scores)[::-1]
        
    ################################### MAIN ALGORITHM LOGIC

    def _selection(self):
        return self.selectionStrategy.apply(self.currentPopulation)
    
    def _crossover(self):
        return self.crossoverStrategy.apply(self._selection())
    
    def _mutation(self):
        return self.mutationStrategy.apply(self._crossover())
    
    def _replacement(self):
        self.currentPopulation = self.replacementStrategy.apply(self.currentPopulation, self._mutation())
    
    def train(self, n_generations):
        for n in range(n_generations):            
            self.bestIndividual = self.currentPopulation[0]
            self.bestScore = self.fitness(self.bestIndividual, **self.fitness_params)
            self.medianIndividual = self.currentPopulation[len(self.currentPopulation)//2]
            self.medianScore = self.fitness(self.medianIndividual, **self.fitness_params)

            self._replacement()
            
            self._sortPopulation()

            #self.logger.log()

            self.generation += 1