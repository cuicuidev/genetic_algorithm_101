import random

from model.strategies.strategy import Strategy

class InitializationStrategy(Strategy):
    pass

class SelectionStrategy(Strategy):
    pass

class CrossoverStrategy(Strategy):
    pass

class MutationStrategy:
    def __init__(self, mutation_rate, severeness=1):
        self.mutation_rate = mutation_rate
        self.severeness = severeness
    
    def _getMutations(self):
        if random.random() < self.mutation_rate:
            # At severity 0, only return 1. At severity 1, ignore mutation_rate and use a 0.5 chance.
            if self.severeness == 0 or random.random() > self.severeness:
                return 1
            else:
                # Here, we're simply ensuring further mutations are equally probable at severity 1.
                original_mut_state = self.mutation_rate
                self.mutation_rate = 0.5
                mutations = 1 + self._getMutations()
                self.mutation_rate = original_mut_state
                return mutations
        return 0


class ReplacementStrategy(Strategy):
    pass

class EndCondition(Strategy):
    pass