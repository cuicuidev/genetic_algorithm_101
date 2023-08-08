import random

from model.strategies.strategies import MutationStrategy

class DeleteMutation(MutationStrategy):
    
    def __init__(self, mutation_rate, severeness, chromosome_min_length):
        super().__init__(mutation_rate, severeness)
        self.chromosome_min_length = chromosome_min_length

    def _mutate(self, child):
        max_index = len(child) - 1
        n_mutations = self._getMutations()

        if not n_mutations:
            return child
        
        for _ in range(n_mutations):
            index = random.randint(0, max_index)
            mutated_child = child[:index] + child[index + 1:]
            if len(mutated_child) == self.chromosome_min_length:
                return child
        return child

class FlipMutation(MutationStrategy):

    def __init__(self, mutation_rate, severeness, gene_pool):
        super().__init__(mutation_rate, severeness)
        self.gene_pool = gene_pool

    def _mutate(self, child):
        n_mutations = self._getMutations()

        child_ = [x for x in child]
        for _ in range(n_mutations):
            index = random.randint(0, len(child_) - 1)
            alternative_genes = [gene for gene in self.gene_pool if gene != child_[index]]
            child_[index] = random.choice(alternative_genes)  # Replace the gene with a different one from the gene pool
        child_ = ''.join(child_)
        return child_

class InverseMutation(MutationStrategy):

    def __init__(self, mutation_rate, severeness):
        super().__init__(mutation_rate, severeness)
    
    def _mutate(self, child):
        n_mutations = self._getMutations()

        child_ = [x for x in child]
        for _ in range(n_mutations):
            index1 = random.randint(0, len(child_) - 1)
            index2 = random.randint(index1, len(child_) - 1)
            child_[index1:index2+1] = reversed(child_[index1:index2+1])
        child_ = ''.join(child_)
        return child_

class SwapMutation(MutationStrategy):

    def __init__(self, mutation_rate, severeness):
        super().__init__(mutation_rate, severeness)
    
    def _mutate(self, child):
        n_mutations = self._getMutations()
        
        child_ = [x for x in child]
        for _ in range(n_mutations):
            index1 = random.randint(0, len(child_) - 1)
            index2 = random.randint(0, len(child_) - 1)
            child_[index1], child_[index2] = child_[index2], child_[index1]  # Swap genes
        child_ = ''.join(child_)
        return child_