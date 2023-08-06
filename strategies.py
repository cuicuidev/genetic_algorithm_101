from abc import ABC, abstractmethod
from typing import Self
import random

class Strategy(ABC):

    @abstractmethod
    def apply(self, **kwargs):
        pass

class SelectionStrategy(Strategy):

    @abstractmethod
    def apply(self, **kwargs):
        pass

# class CrossoverStrategy(Strategy):
#     pass

# class MutationStrategy(Strategy):
#     pass

# class ReplacementStrategy(Strategy):
#     pass

########################################

class TournamentSelection(SelectionStrategy):

    def __init__(self, k, fitness, fitness_params, total_pairs):
        self.k = k
        self.fitness = fitness
        self.fitness_params = fitness_params
        self.total_pairs = total_pairs

    def apply(self, population):
        return self._getPairs(population)
    
    def _getPairs(self, population):
        parents = []
        for i in range(self.total_pairs):
            parent1, parent2 = self._getOnePair(population)
            parents.append((parent1, parent2))
        return parents

    def _getOnePair(self, population):
        parent1 = self._tournament(population)
        parent2 = self._tournament(population)
        return parent1, parent2

    def _tournament(self, population):
        sample = random.sample(population, self.k)
        best = sample[0]
        best_score = self.fitness(string=best, **self.fitness_params)
        for individual in sample:
            score = self.fitness(string=individual, **self.fitness_params)
            if score > best_score:
                best = individual
                best_score = score
        return best

# class BinaryUniformCrossover(CrossoverStrategy):
#     pass

# class PopMutation(MutationStrategy):
#     pass

# class CompleteReplacement(ReplacementStrategy):
#     pass