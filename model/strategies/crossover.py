import random
from model.strategies.strategies import CrossoverStrategy

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
