import random

from model.strategies.strategies import SelectionStrategy

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

class RouletteSelection(SelectionStrategy):
    def __init__(self, fitness, fitness_params, total_pairs):
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
        parent1 = self._roulette(population)
        parent2 = self._roulette(population)
        return parent1, parent2

    def _roulette(self, population):
        total_fitness = sum(self.fitness(string=individual, **self.fitness_params) for individual in population)
        pick = random.uniform(0, total_fitness)
        current = 0
        for individual in population:
            current += self.fitness(string=individual, **self.fitness_params)
            if current > pick:
                return individual