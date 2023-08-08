import random

from model.strategies.strategy import Strategy

class InitializationStrategy(Strategy):
    pass

class SelectionStrategy(Strategy):
    pass

class CrossoverStrategy(Strategy):
    pass

class MutationStrategy(Strategy):
    def __init__(self, mutation_rate, severeness):
        self.mutation_rate = mutation_rate
        self.severeness = severeness
    
    def _getMutations(self):
        if random.random() >= self.mutation_rate:
            return 0

        if random.random() > self.severeness:
            return 1

        # At this point, we are in the multi-mutation scenario (random value is <= severeness)
        original_mut_state = self.mutation_rate
        self.mutation_rate = 0.5
        mutations = 1 + self._getMutations()
        self.mutation_rate = original_mut_state

        return mutations

    def apply(self, children):
        return self._mutateChildren(children)
    
    def _mutateChildren(self, children):
        mutated_children = []
        for child in children:
            mutated_children.append(self._mutate(child))
        return mutated_children
    
    def _mutate(self):
        pass



class ReplacementStrategy(Strategy):
    pass

class EndCondition(Strategy):
    pass