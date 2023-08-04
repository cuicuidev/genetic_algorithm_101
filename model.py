import random
import re

class RegExPatternFinder:
    
    def __init__(self, mutation_rate = 0.05, hostility = 0.5):
        self.mutation_rate = mutation_rate
        self.hostility = hostility
        self.version = 0.9
        self.generation = 0
        self.history = {'generation' : [], 'version' : [], 'best_pattern' : [], 'best_score' : [], 'median_pattern' : [], 'median_score' : [], 'n_survived' : [], 'n_newborns' : []}
        self.current_population = None
        self.best_pattern = None
        self.pattern_size_range = None
        self.survived = None
        self.test_cases = {}
        
    ############################################################################ INITIALIZATION
        
    def initPopulation(self, size = 1000, pattern_size_range = (1,100)):
        population = []
        max_digits = len(str(pattern_size_range[1]))
        
        for i in range(size):
            pattern_size = random.randint(*pattern_size_range)
            chromosome = ''.join([chr(random.randint(32,126)) for x in range(pattern_size)])
            population.append(chromosome)
            
        self.current_population = population
        self.pattern_size_range = pattern_size_range
        
    def setPopulationSize(self, size):
        if len(self.current_population) < size:
            self.current_population.extend(['' for x in range(size - len(self.current_population))])
            return None
        population = self.current_population[:size]
        print(population)
        self.current_population = population
        self._updateVersion()
        
    ############################################################################ TEST CASES
    
    def setTestCases(self, test_cases):
        self.test_cases = test_cases.copy()
        self._updateVersion()
    
    def addOneTestCase(self, test_case):
        self.test_cases[test_case[0]] = test_case[1]
        self._updateVersion()
    
    def updateTestCases(self, test_cases):
        self.test_cases.update(test_cases)
        self._updateVersion()
        
    def removeTestCase(self, string):
        del self.test_cases[string]
        self._updateVersion()
        
    def _updateVersion(self):
        self.version = self.version + 0.1        
        
    
    ############################################################################ FITNESS
    
    def _assertTest(self, pattern, test_case):
        result = bool(re.match(pattern, test_case[0]))
        assertion = result == test_case[1]
        #print(f"Testing: {test_case[0]} | Pattern: {pattern} | Expected: {test_case[1]} | Match: {result}")
        return assertion

    def _fitness(self, pattern):
        total_test_cases = len(self.test_cases)
        successes = 0
        
        try:
            for test_case, expected_output in self.test_cases.items():
                assertion = self._assertTest(pattern, (test_case, expected_output))
                if assertion:
                    successes += 1
        except:
            return -1

        fitness_value = successes / total_test_cases
        #print(f"Fitness: {fitness_value} ({successful_matches}/{total_test_cases} successful matches)")
        return fitness_value
    
    def _sortPopulation(self):
        
        chromosome_fitness_pairs = [[x, self._fitness(x)] for x in self.current_population]
        
        sorted_population = sorted(chromosome_fitness_pairs, key = lambda x : x[1])
        
        
        return sorted_population[::-1]
        
    
    ############################################################################ SELECTION
    
    def _getSurvivors(self):
        
        luck = 0.8
        
        sorted_population = self._sortPopulation()
        middle_point = round(len(sorted_population)*(1 - self.hostility))
        
        best_half = sorted_population[:middle_point]
        worst_half = sorted_population[middle_point:]
        
        survived_best_half = self._kill(best_half, luck)
        survived_worst_half = self._kill(worst_half, 1- luck)
        
        survived = survived_best_half + survived_worst_half
        
        self.survived = [x[0] for x in survived]
        
        return survived
        
        
    def _kill(self, sample, luck):
        survivors = []
        for elem in sample:
            if len(survivors) == 0:
                survivors.append(elem)
                continue
            if random.random() > luck:
                continue
            survivors.append(elem)
        return survivors
    
    
    ############################################################################ BREED
    
    def _breed(self, parent1, parent2, fitness1, fitness2):
        # Determine the shorter and longer parent
        shorter_parent, longer_parent = (parent1, parent2) if len(parent1) <= len(parent2) else (parent2, parent1)

        # Calculate the desired length of the child's chromosome within the range of parent lengths
        min_length = len(shorter_parent)
        max_length = len(longer_parent)
        desired_length = int(min_length + (max_length - min_length) * random.uniform(0, 1) * (fitness1 + fitness2))

        # Randomly decide which parent provides the first slice
        first_parent, second_parent = (parent1, parent2) if random.random() < 0.5 else (parent2, parent1)

        # Calculate a valid crossover point within the range of the shorter parent
        if min_length <= 2:
            crossover_point = min_length  # Avoid crossover if the parent is too short
        else:
            crossover_point = random.randint(1, min_length - 1)

        # Perform crossover to create the child's chromosome
        child_chromosome = first_parent[:crossover_point] + second_parent[crossover_point:desired_length]

        return child_chromosome
    
    def _getChildren(self):
        
        surv = self._getSurvivors()
        survivors = [x[0] for x in surv]
        fitness_scores = [x[1] for x in surv]
        
        middle_point = len(survivors)//2
        
        first_half = survivors[:middle_point]
        last_half = survivors[middle_point:]
        first_scores = fitness_scores[:middle_point]
        last_scores = fitness_scores[middle_point:]
        
        children = []
        for data in zip(first_half, last_half, first_scores, last_scores):
            children.append(self._breed(*data))
        
        return children
    
    
    ############################################################################ MUTATION
    
    def _mutate(self):
        children = self._getChildren()
        
        mutated_children = []
        
        for child in children:
            if random.random() < self.mutation_rate:
                new_child = self._swap(child)
                
                if random.random() < 0.5:
                    index = random.randint(0, len(child))
                    
                    new_child = new_child[:index] + chr(random.randint(32,126)) + new_child[index:]
            
            mutated_children.append(child)
            
        return mutated_children
                
    def _swap(self, child):
        length = len(child)
        index = random.randint(0,length)
        child = child[:index] + chr(random.randint(32,126)) + child[index + 1:]
        return child
    
    ############################################################################ SWAP
    
    def _replacePopulation(self):
        children = self._mutate()
        
        population = self.current_population
        
        survived = self.survived
        
        newborns = []
        
        length = min([len(population)-len(survived), len(children)])
        
        for i in range(length):
            newborns.append(children[i])
        
        new_population = survived + newborns
        
        fill = len(population) - len(new_population)
        
        for i in range(fill):
            pattern_size = random.randint(*self.pattern_size_range)
            chromosome = ''.join([chr(random.randint(32,126)) for x in range(pattern_size)])
            new_population.append(chromosome)
        
        self.current_population = new_population
        
        self.generation += 1
        
        patterns = self._sortPopulation()
        best_pattern = patterns[0]
        median_pattern = patterns[len(patterns)//2]
        
        self.history['best_pattern'].append(best_pattern[0])
        self.history['best_score'].append(best_pattern[1])
        self.history['median_pattern'].append(median_pattern[0])
        self.history['median_score'].append(median_pattern[1])
        self.history['version'].append(self.version)
        self.history['generation'].append(self.generation)
        self.history['n_newborns'].append(len(newborns))
        self.history['n_survived'].append(len(survived))

    ############################################################################ TRAINING
    
    def train(self, iters = 1000):
        for i in range(iters):
            self._replacePopulation()
            if self.generation // 10_000 == 0 and self.generation >= 10_000:
                print(f'Generation {self.generation}')
            
    def getBest(self, top = 10):
        sorted_population = self._sortPopulation()
        return sorted_population[:top]