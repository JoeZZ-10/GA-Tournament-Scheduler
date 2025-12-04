#import class
from ga.population import Population
from data.loadData import LoadData
from ga.Fitness import Fitness
from ga.Selection import Selection
from ga.crossover import Crossover
from ga.mutation import Mutation
from ga.Termination import terminationConditions
import random


loadDataObj = LoadData()
teams = loadDataObj.load_teams()
venues = loadDataObj.load_venues()
timeslots = loadDataObj.load_timeslots()

populationObj = Population()
selectionObj = Selection()
fitnessObj = Fitness()
CrossoverObj = Crossover()
mutationObj = Mutation()

populationSize = 10
generationNum = 0
retainPercentage = 0.2
randomPercentage = 0.05
fittestSolution = None
newGeneration = []

# Generate the population and calculate the fitness for every individual
populationList = populationObj.generate_population(teams, venues, timeslots, populationSize)
for individual in populationList:
    fitnessObj.fitness(individual)

while generationNum != 20:

    # Selection on the whole population
    selectedIndividuals = selectionObj.select_population(populationList, selection_size=5)
    sortedPopulation = sorted(selectedIndividuals,key=lambda ind: ind.fitness_score,reverse=True)

    # keeps a percentage of the top individuals in the new generation
    retainedIndividuals = int(len(populationList) * retainPercentage)
    newGeneration = sortedPopulation [:retainedIndividuals]

    # Adds a few individuals other from the top ones for diversity
    for individual in sortedPopulation[retainedIndividuals:]:
        if randomPercentage > random.random():
            newGeneration.append(individual)

    # Chooses random parents for crossover
    while len(newGeneration) < populationSize:
        index1 = random.randint(0,len(newGeneration)-1)
        index2 = random.randint(0,len(newGeneration)-1)
        if index1 == index2:
            continue
        else:
            parent1 = newGeneration[index1]
            parent2 = newGeneration[index2]
            child1,child2 = CrossoverObj.two_point_crossover(parent1,parent2)
            newGeneration.append(child1)

            if len(newGeneration) < populationSize:
                newGeneration.append(child2)

    # Mutate some individuals
    for individual in newGeneration:
        mutationObj.mutate(individual)

    # calculate fitness for new generation
    for individual in newGeneration:
        fitnessObj.fitness(individual)

    generationNum += 1

    # keeps track of the best solution in the population
    fittestSolution = terminationConditions.checkForSolution(newGeneration)
    if fittestSolution.fitness_score == 10000:
        break
