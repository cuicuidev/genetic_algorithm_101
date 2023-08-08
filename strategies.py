from abc import ABC, abstractmethod
import random

class Strategy(ABC):

    @abstractmethod
    def apply(self):
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

class UniformCrossover(CrossoverStrategy):
    
    def __init__(self, binary = True):
        self.binary = binary

    def apply(self, parents):
        return self._getChildren(parents)
    
    def _getChildren(self, parents):
        children = []
        for parent1, parent2 in parents:
            children.extend(self._uniform(parent1, parent2))
        return children
    
    def _uniform(self, parent1, parent2):
        max_length = max(len(parent1), len(parent2))
        child1 = []
        child2 = [] if self.binary else None

        for i in range(max_length): 
            gen1 = parent1[i % len(parent1)]
            gen2 = parent2[i % len(parent2)]

            if random.randint(0, 1):
                child1.append(gen1)
                if self.binary:
                    child2.append(gen2)
            else:
                child1.append(gen2)
                if self.binary:
                    child2.append(gen1)

        child1 = ''.join(child1)
        if self.binary:
            child2 = ''.join(child2)

        return [child1, child2] if self.binary else [child1]

class OnePointCrossover(CrossoverStrategy):
    
    def __init__(self, binary=True):
        self.binary = binary

    def apply(self, parents):
        return self._getChildren(parents)
    
    def _getChildren(self, parents):
        children = []
        for parent1, parent2 in parents:
            children.extend(self._crossover(parent1, parent2))
        return children
    
    def _crossover(self, parent1, parent2):
        min_length = min(len(parent1), len(parent2))
        
        crossover_point = random.randint(1, min_length-1)
        
        child1 = parent1[:crossover_point] + parent2[crossover_point:min_length]
        if self.binary:
            child2 = parent2[:crossover_point] + parent1[crossover_point:min_length]
            return [child1, child2]
        return [child1]

class TwoPointCrossover(CrossoverStrategy):
    
    def __init__(self, binary=True):
        self.binary = binary

    def apply(self, parents):
        return self._getChildren(parents)
    
    def _getChildren(self, parents):
        children = []
        for parent1, parent2 in parents:
            children.extend(self._crossover(parent1, parent2))
        return children
    
    def _crossover(self, parent1, parent2):
        min_length = min(len(parent1), len(parent2))
        
        point1, point2 = sorted(random.sample(range(1, min_length), 2))
        
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:min_length]
        if self.binary:
            child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:min_length]
            return [child1, child2]
        return [child1]


class PopMutation(MutationStrategy):
    
    def __init__(self, mutation_rate, chromosome_min_length):
        self.mutation_rate = mutation_rate
        self.chromosome_min_length = chromosome_min_length

    def apply(self, children):
        return self._mutateChildren(children)
    
    def _mutateChildren(self, children):
        mutated_children = []
        for child in children:
            mutated_children.append(self._mutate(child))
        return mutated_children

    def _mutate(self, child):
        max_index = len(child) - 1
        if random.random() < self.mutation_rate:
            index = random.randint(0, max_index)
            mutated_child = child[:index] + child[index + 1:]
            return mutated_child if len(mutated_child) > self.chromosome_min_length else child
        return child

class TotalReplacement(ReplacementStrategy):
    
    def __init__(self):
        pass

    def apply(self, population, children):
        return self._totalReplacement(population, children)
    
    def _totalReplacement(self, population, children):
        population = children
        return population