from abc import ABC, abstractmethod
import random

class Strategy(ABC):

    @abstractmethod
    def apply(self, **kwargs):
        pass

class SelectionStrategy(Strategy):
    pass

class CrossoverStrategy(Strategy):
    pass

class MutationStrategy(Strategy):
    pass

class ReplacementStrategy(Strategy):
    pass

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

class BinaryUniformCrossover(CrossoverStrategy):
    
    def __init__(self, anti_twins = True):
        self.anti_twins = anti_twins

    def apply(self, parents):
        return self._getChildren(parents)
    
    def _getChildren(self, parents):
        children = []
        for parent1, parent2 in parents:
            children.extend(self._uniformBinary(parent1, parent2))
        return children
    
    def _uniformBinary(self, parent1, parent2):
        child1 = []
        if self.anti_twins:
            child2 = []
        parent1_ = [x for x in parent1]
        parent2_ = [x for x in parent2]
        for gen1, gen2 in zip(parent1_, parent2_): #TODO: take into account the length of both parents!!!
            if random.randint(0, 1):
                child1.append(gen1)
                if self.anti_twins:
                    child2.append(gen2)
            else:
                child1.append(gen2)
                if self.anti_twins:
                    child2.append(gen1)
        child1 = ''.join(child1)
        if self.anti_twins:
            child2 = ''.join(child2)

        return [child1, child2] if self.anti_twins else [child1]

# class PopMutation(MutationStrategy):
#     pass

# class CompleteReplacement(ReplacementStrategy):
#     pass