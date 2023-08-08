from model.strategies.strategies import ReplacementStrategy


class TotalReplacement(ReplacementStrategy):
    
    def __init__(self):
        pass

    def apply(self, population, children):
        return self._totalReplacement(population, children)
    
    def _totalReplacement(self, population, children):
        population = children
        return population