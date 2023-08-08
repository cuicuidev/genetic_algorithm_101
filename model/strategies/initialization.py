from model.strategies.strategies import InitializationStrategy

import random

class RandomInitialization(InitializationStrategy):

    def __init__(self, gene_pool, min_population_size, max_population_size, min_chromosome_length, max_chromosome_length):
        self.min_population_size = min_population_size
        self.max_population_size = max_population_size
        self.gene_pool = gene_pool
        self.min_chromosome_length = min_chromosome_length
        self.max_chromosome_length = max_chromosome_length

    def apply(self):
        return self._randomInitialization()

    def _randomInitialization(self):
        population = []
        population_size = random.randint(self.min_population_size, self.max_population_size)
        for _ in range(population_size):
            chromosome_size = random.randint(self.min_chromosome_length, self.max_chromosome_length)
            chromosome = ''.join([random.choice(self.gene_pool) for __ in range(chromosome_size)])
            population.append(chromosome)
        return population