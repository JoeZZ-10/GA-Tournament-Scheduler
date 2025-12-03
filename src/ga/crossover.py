import random
import copy
from ga.individual import ScheduleIndividual
class Crossover:

 def uniform_crossover(parent1, parent2):
    rounds = len(parent1.schedule)

    # Deep copy to avoid reference sharing
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    for r in range(rounds):
        if random.random() < 0.5:
            child1.schedule[r], child2.schedule[r] = parent2.schedule[r], parent1.schedule[r]

    return child1, child2

def single_point_crossover(parent1, parent2):
    rounds = len(parent1.schedule)

    # If schedule is too small, return copies
    if rounds < 2:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)

    # Choose crossover point (between rounds)
    point = random.randint(1, rounds - 1)

    # Deep copy to avoid reference sharing
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    # Perform crossover
    child1.schedule = parent1.schedule[:point] + parent2.schedule[point:]
    child2.schedule = parent2.schedule[:point] + parent1.schedule[point:]

    return child1, child2


def two_point_crossover(parent1, parent2):    
    rounds = len(parent1.schedule)

    # If schedule is too small, return copies
    if rounds < 3:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)

    # Choose two crossover points
    point1 = random.randint(1, rounds - 2)
    point2 = random.randint(point1 + 1, rounds - 1)

    # Deep copy to avoid reference sharing
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    # Perform crossover
    child1.schedule = (parent1.schedule[:point1] + 
                       parent2.schedule[point1:point2] + 
                       parent1.schedule[point2:])
    
    child2.schedule = (parent2.schedule[:point1] + 
                       parent1.schedule[point1:point2] + 
                       parent2.schedule[point2:])

    return child1, child2