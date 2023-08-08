import random

from model.strategies.strategies import MutationStrategy

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