import re

def fitness(string, test_cases):
    iters = len(test_cases)
    
    score = 0
    try:
        for key, value in test_cases.items():
            score += int(bool(re.match(string, key)) == value)
    except:
        return -1
    return score / iters