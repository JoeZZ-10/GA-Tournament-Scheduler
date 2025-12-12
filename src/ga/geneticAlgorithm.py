from ga.population import Population
from ga.Fitness import Fitness
from ga.Selection import Selection
from ga.crossover import Crossover
from ga.mutation import Mutation
from ga.Termination import terminationConditions
import random



class GeneticAlgorithm:

    def runAlgorithm (self,teams, venues, timeslots,times, CrossOverType, SlectionType, MutationType):
        populationObj = Population()
        selectionObj = Selection()
        fitnessObj = Fitness()
        CrossoverObj = Crossover()
        mutationObj = Mutation(teams, venues, timeslots, times)
        populationSize = 30
        generationNum = 0
        maximumGenerations = 500
        retainPercentage = 0.2
        randomPercentage = 0.05
        fittestSolution = None
        best_fitness_per_gen = []
        avg_fitness_per_gen = []


        # Generate population and calculate fitness
        populationList = populationObj.generate_population(teams, venues, timeslots,times, populationSize)
        for individual in populationList:
            fitnessObj.fitness(individual)

        while generationNum != maximumGenerations:

            # Selection on the whole population
            selectedIndividuals = selectionObj.select_population(populationList, populationSize, SlectionType)
            sortedPopulation = sorted(selectedIndividuals,key=lambda ind: ind.fitness_score,reverse=True)

            # keeps a percentage of the top individuals in the new generation
            newGeneration = []
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
                    child1,child2 = CrossoverObj.crossover(CrossOverType,parent1,parent2)
                    newGeneration.append(child1)

                    if len(newGeneration) < populationSize:
                        newGeneration.append(child2)

            # Mutate some individuals
            for individual in newGeneration:
                mutationObj.mutate(individual, MutationType)

            # calculate fitness for new generation
            for individual in newGeneration:
                fitnessObj.fitness(individual)

            populationList = newGeneration

            generationNum += 1

            # keeps track of the best solution across all generations
            fittestSolution = terminationConditions.checkForSolution(terminationConditions,newGeneration)
            if fittestSolution.fitness_score == 10000:
                break
            
        if fittestSolution.fitness_score < 0:
            individual.Nosolution = True # to handle the no solutins in the GUI, for mohamed
        # bes and avrage fitness for the plots
        fitness_values = [ind.fitness_score for ind in populationList]

        best_fitness_per_gen.append(max(fitness_values))
        avg_fitness_per_gen.append(sum(fitness_values) / len(fitness_values))

        return fittestSolution