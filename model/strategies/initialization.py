from model.strategies.strategies import InitializationStrategy

import random

class RandomInitialization(InitializationStrategy):

    def __init__(self, population_size, gene_pool, min_chromosome_length, max_chromosome_length):
        self.population_size = population_size
        self.gene_pool = gene_pool
        self.min_chromosome_length = min_chromosome_length
        self.max_chromosome_length = max_chromosome_length

    def apply(self):
        return self._randomInitialization()

    def _randomInitialization(self):
        population = []
        for _ in range(self.population_size):
            chromosome_size = random.randint(self.min_chromosome_length, self.max_chromosome_length)
            chromosome = ''.join([random.choice(self.gene_pool) for __ in range(chromosome_size)])
            population.append(chromosome)
        return population