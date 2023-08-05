from typing import Callable
from time import time

def calculatePhenotypes(genes: str, min_length: int, max_length: int):
    unique_genes = set(genes)
    n_unique_genes = len(unique_genes)

    n_phenotypes = 0
    for length in range(min_length, max_length + 1):
        n_phenotypes += powerOf(n_unique_genes, length)
    
    return n_phenotypes

def powerOf(base, exponent):
    result = 1
    for _ in range(exponent):
        result *= base
    return result

def measureExecTime(func: Callable, iters = 5, **kwargs):
    scores = []
    for i in range(iters):
        start = time()
        result = func(**kwargs)
        end = time()
        scores.append(end-start)
    return sum(scores)/iters
